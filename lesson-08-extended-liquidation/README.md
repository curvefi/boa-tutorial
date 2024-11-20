# Lesson 8: Extended Liquidation 

## [🎥 Curve Titanoboa Tutorial Video 8 : Extended Liquidation 🎬](https://youtu.be/8S0mpw9d2aY)

When a borrower's health is negative and they do not have enough stablecoin as collateral to pay off their debt, you can perform an extended liquidation.  An extended liquidation relies on a callbacker contract to convert their non-stablecoin collateral before performing a liquidation.  This script shows how it is accomplished.

![image](https://github.com/user-attachments/assets/f69a148f-db90-4816-a405-11fb9b5b28dd)

This is part of a series of lessons build atop the [curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo) repository by Curve team member [@Macket](https://github.com/Macket).  


### EXTENDED LIQUIDATION 
When a user is in bad health and their debt is not covered by stablecoin collateral, anybody may run an "extended liquidation" by calling the `liquidate_extended` function.
The `min_x` argument is the minimum amount of stablecoins to receive, to avoid sandwich attack.

```
def liquidate_extended(user: address, min_x: uint256, frac: uint256,
                       callbacker: address, callback_args: DynArray[uint256,5], callback_bytes: Bytes[10**4] = b""):
    """
    @notice Peform a bad liquidation (or self-liquidation) of user if health is not good
    @param min_x Minimal amount of stablecoin to receive (to avoid liquidators being sandwiched)
    @param frac Fraction to liquidate; 100% = 10**18
    @param callbacker Address of the callback contract
    @param callback_args Extra arguments for the callback (up to 5) such as min_amount etc
    """
```


### LIQUIDATION CALLBACKER
To perform an extended liquidation, you must pass the address of a "callbacker" contract responsible for converting collateral into stablecoin to pay off the debt.
This script works off the example provided in [Macket's Liquidation Demo](https://github.com/curvefi/liquidation-demo/blob/master/contracts/HardLiquidatorCurveRouter.vy) that trades collateral through the Curve Router.

## HELPFUL LINKS

* [Macket's curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo)
* [Boa Documentation](https://titanoboa.readthedocs.io/en/latest/api.html)
* [Companion Thread](https://x.com/CurveCap/status/1859207731342889060)
