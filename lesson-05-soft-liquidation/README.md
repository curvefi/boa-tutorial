# Lesson 5: Soft Liquidation 

## [🎥 Curve Titanoboa Tutorial Video 5 : Soft Liquidation 🎬](https://youtu.be/zFuJIcwr6y8)

With our Llama Lend pool and infrastructure set up in the prior four lessons, this unit shows off how to perform soft liquidations by executing basic trades into and out of the AMM.

This lesson also introduce Titanoboa's `anchor` function, which allows you to snapshot the chain at a certain state.


### MATPLOTLIB
[Matplotlib](https://matplotlib.org/) is a comprehensive library for creating static, animated and interactive visualizations that works well with Jupyter Notebooks


### ANCHOR
The Titanoboa `anchor` function is a context manager that snapshots the state and the VM, and reverts to the snapshot on exit

```
>>> import boa
>>> src = """
... value: public(uint256)
... """
>>> contract = boa.loads(src)
>>> contract.value()
0

>>> with boa.env.anchor():
...     contract.eval("self.value += 1")
...     contract.value()
...
1

>>> contract.value()
0
```


### READ_USER_TICK_NUMBERS
For charting, the demo notebook determines the charting range by reading the AMM's `read_user_tick_numbers` function.
The function accepts a user address and returns the lowest and highest band the user has deposited into.

```
def read_user_tick_numbers(user: address) -> int256[2]:
    """
    @notice Unpacks and reads user tick numbers
    @param user User address
    @return Lowest and highest band the user deposited into
    """
```


### AMM P_ORACLE FUNCTIONS
In the demo notebook we calculate the price boundaries of each band using the AMM's `p_oracle_up` and `p_oracle_down` functions.
These functions return the edges of the band when the current price of the AMM is equal to the oracle price (a steady state).

The grid of bands is set for p_oracle values such as:
* `p_oracle_up(n) = base_price * ((A - 1) / A) ** n`
* `p_oracle_down(n) = p_oracle_up(n) * (A - 1) / A = p_oracle_up(n + 1)`


```
def p_oracle_up(n: int256) -> uint256:
    """
    @notice Highest oracle price for the band to have liquidity when p = p_oracle
    @param n Band number (can be negative)
    @return Price at 1e18 base
    """

def p_oracle_down(n: int256) -> uint256:
    """
    @notice Lowest oracle price for the band to have liquidity when p = p_oracle
    @param n Band number (can be negative)
    @return Price at 1e18 base
    """
```


### BANDS_Y
The AMM's `bands_y` is a Vyper HashMap that stores the amount of coin y (in this case the collateral token) deposited in a given band.

```
bands_y: public(HashMap[int256, uint256])
```


### GET_DY
The AMM's `get_dy` function is a method that calculates the output of a exchange given an amount of input coin

```
def get_dy(i: uint256, j: uint256, in_amount: uint256) -> uint256:
    """
    @notice Method to use to calculate out amount
    @param i Input coin index
    @param j Output coin index
    @param in_amount Amount of input coin to swap
    @return Amount of coin j to give out
    """
```


### GET_DX
The AMM's `get_dx` function calculates the amount of input coin necessary to get a desired output amount

```
def get_dx(i: uint256, j: uint256, out_amount: uint256) -> uint256:
    """
    @notice Method to use to calculate in amount required to receive the desired out_amount
    @param i Input coin index
    @param j Output coin index
    @param out_amount Desired amount of output coin to receive
    @return Amount of coin i to spend
    """
    # i = 0: borrowable (USD) in, collateral (ETH) out; going up
    # i = 1: collateral (ETH) in, borrowable (USD) out; going down
```


### EXCHANGE
After granting approvals, the AMM's `exchange` function trades a quantity of tokens

```
def exchange(i: uint256, j: uint256, in_amount: uint256, min_amount: uint256, _for: address = msg.sender) -> uint256[2]:
    @notice Exchanges two coins, callable by anyone
    @param i Input coin index
    @param j Output coin index
    @param in_amount Amount of input coin to swap
    @param min_amount Minimal amount to get as output
    @param _for Address to send coins to
    @return Amount of coins given in/out
```



## HELPFUL LINKS

* [Matplotlib](https://matplotlib.org/)
* [Boa Anchor Documentation](https://titanoboa.readthedocs.io/en/latest/api.html#boa.environment.Env.anchor)
* [Llama Lend AMM](https://github.com/curvefi/curve-stablecoin/blob/master/contracts/AMM.vy)

