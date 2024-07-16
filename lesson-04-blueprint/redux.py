import boa, os
from dotenv import load_dotenv
from snekmate.tokens import ERC20

VERBOSE = False


def verbose_print(text):
    if VERBOSE:
        print(text)


def display_erc20(balance):
    return f"{balance / 10 ** 18:,.0f}"


def lesson3():
    # Constants
    load_dotenv(".env")
    RPC_URL = f"https://arb-mainnet.g.alchemy.com/v2/{os.getenv('ARB_ALCHEMY_KEY')}"
    ARBISCAN_KEY = os.getenv("ARBISCAN_KEY")
    ARBISCAN_API = "https://api.arbiscan.io/api"
    FACTORY_ADDR = "0xcaec110c784c9df37240a8ce096d352a75922dea"

    # Fork an RPC Node
    boa.env.fork(RPC_URL)
    verbose_print(f"Current block: {boa.env.evm.patch.block_number}")

    # Redeploy collateral token from lesson 1
    collateral_token = ERC20.deploy("Vyper wif hat", "VWIF", 100_000_000, "", "")
    verbose_print(
        f"Deployed to {collateral_token.address} "
        + f"and minted\n{collateral_token.balanceOf(collateral_token.owner()) / 10**18:,.0f} "
        + f"${collateral_token.symbol()} "
        + f"tokens to token owner {collateral_token.owner()}"
    )

    # Load Factory Contract
    factory = boa.from_etherscan(FACTORY_ADDR, "Factory", ARBISCAN_API, ARBISCAN_KEY)

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

    # Deploy Dummy Oracle
    oracle = dummy_oracle.deploy(boa.env.eoa, 10**18)
    verbose_print(
        f"Dummy oracle deployed to {oracle.address} with oracle price of {oracle.price_w() / 10**18}"
    )

    # Deploy
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
    return vault_addr, collateral_token, factory
