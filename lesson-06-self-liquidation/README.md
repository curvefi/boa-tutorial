# Lesson 6: Self Liquidation 

## [🎥 Curve Titanoboa Tutorial Video 6 : Self-Liquidation 🎬](https://youtu.be/aPkApyN3-GM)

When your health turns negative, a well-timed self-liquidation can perform like a stop-loss mechanism.  This lesson shows off the basics for manually running a self-liquidation.

This lesson also introduce Titanoboa's `time_travel` function, which allows you to fast forward a specified timeframe or number of blocks.


## TITANOBOA FUNCTIONALITY

### TIME TRAVEL
Fast forward, increase the chain timestamp and block number.
Further details available in the [Titanoboa documentation](https://titanoboa.readthedocs.io/en/latest/api.html#boa.environment.Env.time_travel)

```
time_travel(seconds: int = None, blocks: int = None, block_delta: int = 12)
```


## LLAMA LEND CONTROLLER FUNCTIONALITY

### TOKENS_TO_LIQUIDATE
Determine stablecoin quantity needed to liquidate a user.
This amount may be different if a user is calling this function on their own loan (ie self-liquidation).

```
def tokens_to_liquidate(user: address, frac: uint256 = 10 ** 18) -> uint256:
    """
    @notice Calculate the amount of stablecoins to have in liquidator's wallet to liquidate a user
    @param user Address of the user to liquidate
    @param frac Fraction to liquidate; 100% = 10**18
    @return The amount of stablecoins needed
    """
```


### LIQUIDATE
Perform a liquidation on a user in bad health.

```
def liquidate(user: address, min_x: uint256):
    """
    @notice Peform a bad liquidation (or self-liquidation) of user if health is not good
    @param min_x Minimal amount of stablecoin to receive (to avoid liquidators being sandwiched)
    """
```


## LIQUIDITY POOL FUNCTIONALITY


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

* [Boa Time Travel Documentation](https://titanoboa.readthedocs.io/en/latest/api.html#boa.environment.Env.time_travel)
* [crvUSD Llama Lend Controller](https://arbiscan.io/address/0x2287b7b2bF3d82c3ecC11ca176F4B4F35f920775#code)
* [Curve Liquidity Pool](https://arbiscan.io/address/0x934791f7F391727db92BFF94cd789c4623d14c52#code)

