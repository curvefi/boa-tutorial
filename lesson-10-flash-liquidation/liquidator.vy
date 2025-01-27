#  pragma version 0.4.0

"""
@title Flash Liquidator
@license MIT
@author Curve Finance
@notice You can use this contract to liquidate the deadbeat user
"""

from ethereum.ercs import IERC20

interface FlashLender:
    def flashLoan(
        receiver: address, token: address, amount: uint256, data: Bytes[10**5]
    ) -> bool: nonpayable


interface Controller:
    def liquidate(user: address, min_x: uint256): nonpayable
    def collateral_token() -> IERC20: view
    def borrowed_token() -> IERC20: view


interface Pool:
    def get_dy(i: uint256, j: uint256, dx: uint256) -> uint256: view
    def exchange(
        i: uint256,
        j: uint256,
        dx: uint256,
        min_dy: uint256,
    ) -> uint256: nonpayable


# Contracts
flashlender: public(FlashLender)
controller: public(Controller)
liquidity_pool: public(Pool)

# Tokens
crvusd: public(IERC20)
collateral: public(IERC20)

# EOAs
victim: public(address)
hero: public(address)


@deploy
def __init__(
    _flashlender_addr: address, _controller_addr: address, _pool_addr: address
):
    # Initialize contracts
    self.flashlender = FlashLender(_flashlender_addr)
    self.controller = Controller(_controller_addr)
    self.liquidity_pool = Pool(_pool_addr)

    # Initialize tokens
    self.collateral = staticcall self.controller.collateral_token()
    self.crvusd = staticcall self.controller.borrowed_token()


@external
def run_liquidation(victim: address, hero: address):
    """
    @notice Liquidate a crvUSD borrower in bad health
    @dev Trigger the flashlender, which calls back to this contract's `onFlashLoan()`
    @param victim Address of the user subject to liquidation
    """

    # Set addresses
    self.victim = victim
    self.hero = hero

    # Run flashloan
    extcall self.flashlender.flashLoan(
        self,
        self.crvusd.address,
        staticcall self.crvusd.balanceOf(self.flashlender.address),
        empty(Bytes[10**5]),
    )


@external
def onFlashLoan(
    sender_addr: address,
    crvusd_addr: address,
    amount: uint256,
    fee: uint256,
    data: Bytes[10**5],
) -> bool:
    """
    @notice The flashlender sends the crvUSD while calling this
    @dev Standardized function, must return the entire loan in the same block or revert
    @param sender_addr This contract's address
    @param crvusd_addr Address of crvUSD stablecoin
    @param amount Value of flashloan (here pulling/returning entire balance)
    @param fee crvUSD flashlender set to 0
    @param data Optional supplemental data
    @return True on success or revert
    """
    assert sender_addr == self

    # Set approvals if needed
    self._approve_self(self.crvusd, self.controller.address)
    self._approve_self(self.collateral, self.liquidity_pool.address)

    # Liquidate the user
    extcall self.controller.liquidate(self.victim, 0)

    # Trade all received collateral into stablecoin
    _balance: uint256 = (
        staticcall self.collateral.balanceOf(self) - 500 * 10**18
    )
    _expected: uint256 = staticcall self.liquidity_pool.get_dy(1, 0, _balance)
    extcall self.liquidity_pool.exchange(1, 0, _balance, _expected)

    # Repay the flash loan
    extcall self.crvusd.transfer(msg.sender, amount)

    # Anything left to the liquidator
    extcall self.crvusd.transfer(
        self.hero, staticcall self.crvusd.balanceOf(self)
    )
    extcall self.collateral.transfer(
        self.hero, staticcall self.collateral.balanceOf(self)
    )
    return True


@internal
def _approve_self(_token: IERC20, _spender: address):
    """
    @notice Helper function to set max ERC20 approval if missing
    @param _token Token to approve
    @param _spender Authorized spender
    """
    if staticcall _token.allowance(self, _spender) == 0:
        extcall _token.approve(
            _spender, max_value(uint256), default_return_value=True
        )
