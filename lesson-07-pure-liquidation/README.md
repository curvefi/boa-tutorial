# Lesson 7: Pure Liquidation 

## [🎥 Curve Titanoboa Tutorial Video 7 : Pure Liquidation 🎬](https://youtu.be/5uiPaXfXIw4)

Pure liquidation in LLAMMA is possible when a borrower's health is negative and their collateral has been converted to stablecoin in a quantity that covers the outstanding debt. In such circumstances, it is possible for anybody to directly perform a "pure liquidation" of the borrower.  This contrasts with cases where the user's collateral has not been fully converted to crvUSD, and more extended liquidation mechanisms must be used.

This and subsequent lessons build atop the [curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo) repository by Curve team member [@Macket](https://github.com/Macket).  

New Titanoboa concepts introduced in this lesson include the `generate_address` and the `load_abi` functions.


## TITANOBOA FUNCTIONALITY
Further details may be found in the [Titanoboa documentation](https://titanoboa.readthedocs.io/)

### GENERATE ADDRESS
Generate an EVM address.  This address can optionally be aliased, and a seed can optionally be set to randomize address generation.

```
> boa.env.set_random_seed(100)
> boa.env.generate_address('optional alias')
```

### LOAD ABI
Built in boa function to load an ABI from a json file and create an `ABIContractFactory`, which can interface with deployed contracts.

```
> implementation = boa.load_abi('abi_file.json', name="MyContract")
> my_contract = implementation.at('0xdeadbeef...')
```


## LLAMA LEND CONTROLLER FUNCTIONALITY

### USER STATE

Calling `user_state` on Llama Lend controllers returns four key loan parameters in a single call

0. Amount of `collateral` the user owns
1. Amount of `stablecoin` the user owns
2. Current amount of user `debt`
3. Number of bands (`n`) across which the user has spread collateral

```
> controller.user_state(address)
```

### PURE LIQUIDATION 
When a user is in bad health and their debt is covered by collateral converted into stablecoins, anybody may run a "pure liquidation" by calling the `liquidate` function.
The `min_x` argument is the minimum amount of stablecoins to receive, to avoid sandwich attack.

```
def liquidate(user: address, min_x: uint256):
    """
    @notice Peform a bad liquidation (or self-liquidation) of user if health is not good
    @param min_x Minimal amount of stablecoin to receive (to avoid liquidators being sandwiched)
    """
```


## HELPFUL LINKS

* [Macket's curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo)
* [Boa Documentation](https://titanoboa.readthedocs.io/en/latest/api.html)
* [crvUSD Llama Lend Controller](https://arbiscan.io/address/0x2287b7b2bF3d82c3ecC11ca176F4B4F35f920775#code)
* [Curve Liquidity Pool](https://arbiscan.io/address/0x934791f7F391727db92BFF94cd789c4623d14c52#code)

