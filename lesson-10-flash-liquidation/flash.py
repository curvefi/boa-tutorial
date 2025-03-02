import os
import time

import boa
from boa.contracts.abi.abi_contract import ABIContractFactory
from boa.explorer import fetch_abi_from_etherscan
from dotenv import load_dotenv
from snekmate.tokens import ERC20

SLEEP_DELAY = 1
VERBOSE = False

load_dotenv(".env")
ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")
ETHERSCAN_API = "https://api.etherscan.io/api"


def verbose_print(text):
    if VERBOSE:
        print(text)


def display_erc20(balance):
    return f"{balance / 10 ** 18:,.0f}"


def load_from_impl(contract_addr, abi_addr, name=None):
    if name is None:
        name = contract_addr
    time.sleep(SLEEP_DELAY)
    abi = fetch_abi_from_etherscan(abi_addr, ETHERSCAN_API, ETHERSCAN_KEY)
    time.sleep(SLEEP_DELAY)
    return ABIContractFactory.from_abi_dict(abi, name=name).at(contract_addr)


def crvusd_mint(crvusd, user, amount):
    whale = "0xA920De414eA4Ab66b97dA1bFE9e6EcA7d4219635"  # crvusd ETH controller
    crvusd.transfer(user, amount, sender=whale)


def flash_setup():
    # LOAD CONSTANTS
    user = boa.env.eoa
    RPC_URL = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ETH_ALCHEMY_KEY')}"
    FACTORY_ADDR = "0xea6876dde9e3467564acbee1ed5bac88783205e0"

    # FORK AN RPC NODE
    boa.env.fork(RPC_URL)
    verbose_print(f"Current block: {boa.env.evm.patch.block_number}")

    # REDEPLOY COLLATERAL TOKEN FROM LESSON 1
    collateral_token = ERC20.deploy("Vyper wif hat", "VWIF", 100_000_000, "", "")
    verbose_print(
        f"Deployed to {collateral_token.address} "
        + f"and minted\n{collateral_token.balanceOf(collateral_token.owner()) / 10**18:,.0f} "
        + f"${collateral_token.symbol()} "
        + f"tokens to token owner {collateral_token.owner()}"
    )

    # LOAD FACTORY CONTRACT
    factory = boa.from_etherscan(FACTORY_ADDR, "Factory", ETHERSCAN_API, ETHERSCAN_KEY)

    src = """
    price: public(uint256)
    ADMIN: immutable(address)

    @external
    def __init__(admin: address, price: uint256):
        self.price = price
        ADMIN = admin

    @external
    def price_w() -> uint256:
        # State-changing price oracle in case we want to include EMA
        return self.price

    @external
    def set_price(price: uint256):
        assert msg.sender == ADMIN
        self.price = price
    """
    dummy_oracle = boa.loads_partial(src, "DummyOracle")

    # DEPLOY DUMMY ORACLE
    oracle = dummy_oracle.deploy(boa.env.eoa, 10**18)
    verbose_print(
        f"Dummy oracle deployed to {oracle.address} with oracle price of {oracle.price_w() / 10**18}"
    )

    # DEPLOY VAULT
    vault_addr = factory.create(
        factory.STABLECOIN(),
        collateral_token,
        1000,
        500000000000000,
        13000000000000000,
        10000000000000000,
        oracle,
        "VyperWif",
        0,
        4756468797,
    )
    verbose_print(f"VyperWIF Vault deployed to {vault_addr}")

    # LOAD THE LLAMA LEND VAULT AND CONTROLLER FROM BLUEPRINT ABI
    vault = load_from_impl(vault_addr, factory.vault_impl(), "VyperWifVault")
    controller = load_from_impl(
        vault.controller(), factory.controller_impl(), "VyperWifController"
    )
    amm = load_from_impl(vault.amm(), factory.amm_impl(), "VyperWifAMM")

    verbose_print(f"{vault._name} loaded: {vault.address}")
    verbose_print(f"{controller._name} loaded: {controller.address}")
    verbose_print(f"{amm._name} loaded: {amm.address}")

    # MINT CRVUSD
    vault_crvusd_balance = 100_000 * 10**18
    time.sleep(SLEEP_DELAY)
    crvusd = boa.from_etherscan(
        factory.STABLECOIN(), "crvUSD", ETHERSCAN_API, ETHERSCAN_KEY
    )

    verbose_print(f"Init $crvUSD balance: {display_erc20(crvusd.balanceOf(user))}")
    crvusd_mint(crvusd, user, vault_crvusd_balance)
    verbose_print(f"Final $crvUSD balance: {display_erc20(crvusd.balanceOf(user))}")

    # DEPOSIT CRVUSD TO THE VAULT CONTRACT
    verbose_print("Init $crvUSD balance")
    verbose_print(f" • User: {display_erc20(crvusd.balanceOf(user))}")
    verbose_print(f" • Controller: {display_erc20(crvusd.balanceOf(controller))}")

    # Approve
    crvusd.approve(vault, crvusd.balanceOf(user))

    # Supply $crvUSD
    vault.deposit(crvusd.balanceOf(user))

    verbose_print("Final $crvUSD balance")
    verbose_print(f" • User: {display_erc20(crvusd.balanceOf(user))}")
    verbose_print(f" • Controller: {display_erc20(crvusd.balanceOf(controller))}")

    # CREATE A CRVUSD LOAN USING YOUR VYPERWIF MEMECOIN AS COLLATERAL
    verbose_print(
        f"Init $VyperWIF balance \n • User: {display_erc20(collateral_token.balanceOf(user))}"
    )
    verbose_print(f" • AMM: {display_erc20(collateral_token.balanceOf(vault.amm()))}")

    n_bands = 30

    # Approve
    collateral_amount = 100_000 * 10**18
    borrow_amount = controller.max_borrowable(collateral_amount, n_bands)
    collateral_token.approve(controller, collateral_amount)

    # Borrow
    controller.create_loan(collateral_amount, borrow_amount, n_bands)

    verbose_print(
        f"Final $VyperWIF balance \n • User: {display_erc20(collateral_token.balanceOf(user))}"
    )
    verbose_print(f" • AMM: {display_erc20(collateral_token.balanceOf(vault.amm()))}")

    # CREATE CURVE POOL
    time.sleep(SLEEP_DELAY)
    pool_factory = boa.from_etherscan(
        "0x98ee851a00abee0d95d08cf4ca2bdce32aeaaf7f",
        "Factory",
        ETHERSCAN_API,
        ETHERSCAN_KEY,
    )
    init_count = pool_factory.pool_count()
    implementation_id = 0

    pool_factory.deploy_pool(
        "SnekWIF/crvUSD",
        "SnekUSD",
        [factory.STABLECOIN(), collateral_token],
        implementation_id,
        400_000,  # A Parameter
        int(0.000145 * 10**18),  # Gamma
        int(0.26 * 10**8),  # Mid Fee
        int(0.45 * 10**8),  # Out Fee
        int(0.00023 * 10**18),  # Fee Gamma
        int(0.000002 * 10**18),  # Allowed Extra Profit
        int(0.000146 * 10**18),  # Adjustment Step
        600,  # Moving Average Time
        amm.price_oracle(),
    )

    assert pool_factory.pool_count() > init_count

    liquidity_pool_addr = pool_factory.pool_list(pool_factory.pool_count() - 1)
    liquidity_pool = load_from_impl(
        liquidity_pool_addr,
        pool_factory.pool_implementations(implementation_id),
        "VyperWIFPool",
    )

    verbose_print(f"Successfully deployed Snek Pool to {liquidity_pool_addr}")

    # SEED CURVE POOL
    pool_crvusd_balance = int(10_000_000 * 10**18)
    pool_token_balance = int(amm.price_oracle() * pool_crvusd_balance / 10**18)

    assert collateral_token.balanceOf(user) > pool_token_balance
    crvusd_mint(crvusd, user, pool_crvusd_balance)

    # Approve
    crvusd.approve(liquidity_pool, pool_crvusd_balance)
    collateral_token.approve(liquidity_pool, pool_token_balance)

    # Seed
    liquidity_pool.add_liquidity([pool_crvusd_balance, pool_token_balance], 0)
    verbose_print(
        f"Deposited and received {display_erc20(liquidity_pool.balanceOf(user))} LP tokens"
    )

    return (
        vault,
        controller,
        amm,
        oracle,
        factory,
        liquidity_pool,
        collateral_token,
        crvusd,
    )
