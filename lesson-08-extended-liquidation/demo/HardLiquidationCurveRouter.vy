# @version 0.3.10

interface ERC20:
    def transfer(_to: address, _value: uint256) -> bool: nonpayable
    def approve(_spender: address, _value: uint256) -> bool: nonpayable
    def balanceOf(_for: address) -> uint256: view
    def allowance(_owner: address, _spender: address) -> uint256: view

interface OldController:  # Has use_eth arg
    def liquidate_extended(user: address, min_x: uint256, frac: uint256, use_eth: bool, callbacker: address, callback_args: DynArray[uint256,5]): nonpayable

interface Controller:
    def liquidate_extended(user: address, min_x: uint256, frac: uint256, callbacker: address, callback_args: DynArray[uint256,5]): nonpayable
    def collateral_token() -> ERC20: view
    def borrowed_token() -> ERC20: view


ROUTER: immutable(address)

controller: Controller
calldata: Bytes[10**5]


@external
def __init__(_router: address):
    ROUTER = _router


@external
def callback_liquidate(user: address, stablecoins: uint256, collateral: uint256, debt: uint256, callback_args: DynArray[uint256, 5]) -> uint256[2]:
    assert msg.sender == self.controller.address

    collateral_token: ERC20 = self.controller.collateral_token()
    borrowed_token: ERC20 = self.controller.borrowed_token()
    if collateral_token.allowance(self, ROUTER) == 0:
        collateral_token.approve(ROUTER, max_value(uint256), default_return_value=True)
    if borrowed_token.allowance(self, self.controller.address) == 0:
        borrowed_token.approve(self.controller.address, max_value(uint256), default_return_value=True)

    raw_call(ROUTER, self.calldata)
    borrowed_amt: uint256 = borrowed_token.balanceOf(self)

    return [borrowed_amt, 0]


@external
def liquidate(user: address, min_x: uint256, frac: uint256, controller: address, calldata: Bytes[10**5], has_use_eth: bool = False, _for: address = msg.sender) -> uint256[2]:
    self.controller = Controller(controller)
    self.calldata = calldata

    if has_use_eth:
        OldController(self.controller.address).liquidate_extended(user, min_x, frac, False, self, [])
    else:
        self.controller.liquidate_extended(user, min_x, frac, self, [])

    collateral_token: ERC20 = self.controller.collateral_token()
    borrowed_token: ERC20 = self.controller.borrowed_token()
    collateral_amt: uint256 = collateral_token.balanceOf(self)
    borrowed_amt: uint256 = borrowed_token.balanceOf(self)
    if collateral_amt > 0:
        assert collateral_token.transfer(_for, collateral_amt)
    if borrowed_amt > 0:
        assert borrowed_token.transfer(_for, borrowed_amt)

    return [borrowed_amt, collateral_amt]
