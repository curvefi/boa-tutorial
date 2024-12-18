import boa

ETH_DRPC = "https://eth.drpc.org"
LLAMALEND_FACTORY = "0xeA6876DDE9e3467564acBeE1Ed5bac88783205E0"
CURVE_ROUTER = "0x16C6521Dff6baB339122a0FE25a9116693265353"
SWAP_DATA = {
    "route": [
        "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # WBTC
        "0xf5f5b97624542d72a9e06f04804bf81baa15e2b4",  # TricryptoUSDT pool
        "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
        "0x390f3595bca2df7d23783dfd126427cceb997bf4",  # crvUSD/USDT pool
        "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e",  # crvUSD
    ] + ["0x0000000000000000000000000000000000000000"] * 6,
    "swap_params": [[1, 0, 1, 30, 3], [0, 1, 1, 1, 2]] + [[0, 0, 0, 0, 0]] * 3,
    "pools": [
         "0xf5f5b97624542d72a9e06f04804bf81baa15e2b4",  # TricryptoUSDT pool
         "0x390f3595bca2df7d23783dfd126427cceb997bf4",  # crvUSD/USDT pool
     ] + ["0x0000000000000000000000000000000000000000"] * 3
}

if __name__ == '__main__':
    RPC_URL = f"https://eth-mainnet.g.alchemy.com/v2/j297EkGkbCm4gXStDjfgmuxv7EX8ucYZ"
    #boa.env.fork(ETH_DRPC)
    boa.env.fork(RPC_URL)

    factory_impl = boa.load_abi("interfaces/Factory.json", name="FactoryMock")
    vault_impl = boa.load_abi("interfaces/Vault.json", name="VaultMock")
    controller_impl = boa.load_abi("interfaces/Controller.json", name="ControllerMock")
    amm_impl = boa.load_abi("interfaces/AMM.json", name="AMMMock")
    coin_impl = boa.load_abi("interfaces/ERC20.json", name="ERC20Mock")

    # --- Users ---

    admin = boa.env.generate_address()
    borrower = boa.env.generate_address()
    trader = boa.env.generate_address()
    liquidator = boa.env.generate_address()

    # --- Deploy the new WBTC long market ---

    factory = factory_impl.at(LLAMALEND_FACTORY)
    crvusd_address = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"
    wbtc_address = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    A = 75
    fee = 1500000000000000  # 15 bps
    loan_discount = 65000000000000000  # 6.5 %
    liquidation_discount = 35000000000000000  # 3.5 %

    with boa.env.prank(admin):
        price_oracle = boa.load("contracts/DummyPriceOracle.vy", admin, 65_000 * 10**18)
        vault_address = factory.create(
            crvusd_address,
            wbtc_address,
            A,
            fee,
            loan_discount,
            liquidation_discount,
            price_oracle.address,
            "WBTC Long Example",
        )

    vault = vault_impl.at(vault_address)
    controller = controller_impl.at(vault.controller())
    amm = amm_impl.at(vault.amm())

    # --- Load crvUSD into the new market ---

    supply_amount = 10**8 * 10**18  # 100M
    crvusd = coin_impl.at(crvusd_address)
    crvusd.transfer(admin, supply_amount, sender="0xA920De414eA4Ab66b97dA1bFE9e6EcA7d4219635")  # crvusd ETH controller
    with boa.env.prank(admin):
        crvusd.approve(vault, supply_amount)
        vault.deposit(supply_amount)

    # --- Create loan close to oracle price ---

    collateral_amount = 200 * 10**8  # 200 BTC
    wbtc = coin_impl.at(wbtc_address)
    wbtc.transfer(borrower, collateral_amount, sender="0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8")  # AAVE

    max_borrowable = controller.max_borrowable(collateral_amount, 30)
    with boa.env.prank(borrower):
        wbtc.approve(controller, collateral_amount)
        controller.create_loan(collateral_amount, max_borrowable, 30)

    # --- Dump and trade ---

    print(supply_amount)
    sender = '0x4e59541306910ad6dc1dac0ac9dfb29bd9f15c67' 
    print(crvusd.balanceOf(sender))
    assert crvusd.balanceOf(sender) > supply_amount
    crvusd.transfer(trader, supply_amount, sender="0x4e59541306910ad6dc1dac0ac9dfb29bd9f15c67")  # crvusd WBTC controller
    wbtc.transfer(trader, collateral_amount, sender="0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8")  # AAVE

    with boa.env.prank(trader):
        crvusd.approve(amm, 2**256 - 1)
        wbtc.approve(amm, 2**256 - 1)

    [p_up, p_down] = controller.user_prices(borrower)
    p_mid = (p_up + p_down) // 2
    p_o = 65_000 * 10**18

    while controller.health(borrower) > 0:
        if p_o == p_mid:
            p_o = p_o * 20 // 19
        elif p_o * 19 // 20 < p_mid:
            p_o = p_mid
        else:
            p_o = p_o * 19 // 20

        price_oracle.set_price(p_o, sender=admin)
        boa.env.time_travel(seconds=600)
        trade_amount, is_pump = amm.get_amount_for_price(p_o)
        i = 0  # crvUSD in
        j = 1  # WBTC out
        if not is_pump:
            i, j = j, i  # WBTC in and crvUSD out

        amm.exchange(i, j, trade_amount, 0, sender=trader)
        print("Borrower health:", controller.health(borrower) / 10 ** 16, "%")

    # --- Liquidate ---

    curve_router_impl = boa.load_abi("interfaces/CurveRouter.json", name="CurveRouterMock")
    curve_router = curve_router_impl.at(CURVE_ROUTER)
    hard_liquidator = boa.load("contracts/HardLiquidatorCurveRouter.vy", CURVE_ROUTER)

    state_wbtc, state_crvusd, debt, N = controller.user_state(borrower)
    tokens_to_liquidate = debt - state_crvusd
    wbtc_required = curve_router.get_dx(SWAP_DATA["route"], SWAP_DATA["swap_params"], tokens_to_liquidate, SWAP_DATA["pools"])

    print(f"\nUnhealthy user state: {state_wbtc / 10**8} WTBC, {state_crvusd / 10**18} crvUSD, {debt / 10**18} debt")
    print(f"Tokens to liquidate: {tokens_to_liquidate / 10**18} crvUSD")
    print(f"WBTC required: {wbtc_required / 10**8} WBTC")
    print(f"WBTC required > borrower collateral! We can't liquidate fully, so let's liquidate 10%.\n")

    frac = 0.1
    h = controller.liquidation_discounts(borrower) / 10 ** 18
    f_remove = ((1 + h / 2) / (1 + h) * (1 - frac) + frac) * frac  # < frac

    print(f"In case of partial liquidation we get less collateral and thus increase user's health.\n"
          f"In this example we get {f_remove * 100} % of collateral and borrowed assets "
          f"from user's position, but have to repay {frac * 100} % of debt")

    wbtc_to_sell = int(state_wbtc * f_remove)
    expected = curve_router.get_dy(SWAP_DATA["route"], SWAP_DATA["swap_params"], wbtc_to_sell)
    calldata = curve_router.exchange.prepare_calldata(SWAP_DATA["route"], SWAP_DATA["swap_params"], wbtc_to_sell, expected * 999 // 1000)

    print(f"WBTC to sell: {wbtc_to_sell / 10 ** 8} WBTC")
    print(f"Expected: {expected / 10 ** 18} crvUSD")
    print(f"Liquidator balances: {wbtc.balanceOf(liquidator) / 10 ** 8} WBTC, {crvusd.balanceOf(liquidator) / 10 ** 18} crvUSD")
    print("Borrower health:", controller.health(borrower) / 10 ** 16, "%")

    # frac = 10**17 (10 %), partial liquidation
    hard_liquidator.liquidate(borrower, int(state_crvusd * f_remove) * 999 // 1000, 10**17, controller, calldata, sender=liquidator)
    print("\nPARTIAL LIQUIDATION HAPPENED!!!\n")

    state_wbtc, state_crvusd, debt, N = controller.user_state(borrower)

    print("Borrower health:", controller.health(borrower) / 10 ** 16, "%")
    print(f"Partially liquidated user state: {state_wbtc / 10 ** 8} WTBC, {state_crvusd / 10 ** 18} crvUSD, {debt / 10 ** 18} debt")
    print(f"Liquidator balances: {wbtc.balanceOf(liquidator) / 10**8} WBTC, {crvusd.balanceOf(liquidator) / 10**18} crvUSD")
