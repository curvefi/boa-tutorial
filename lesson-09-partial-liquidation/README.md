# Lesson 9: Extended Liquidation 

## [🎥 Curve Titanoboa Tutorial Video 9 : Extended Liquidation 🎬](https://youtu.be/UcPmIEMQ5BA)

LLAMMA borrowers in bad health can be "partially" liquidated.  The process works similar to other liquidations, except a "liquidation discount" applies.

This is the third in a series of lessons that build atop the [curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo) repository by Curve team member [@Macket](https://github.com/Macket).  The source script is provided in the [demo](/lesson-09-partial-liquidation/demo/partial-liquidation-example.py) folder.

### LIQUIDATION DISCOUNT
When `frac`, a liquidation fraction, is passed during a liquidation, the controller calls the `_get_f_remove()` function to calculate the liquidation discount.

The controller documents it:

```
    # Withdraw sender's stablecoin and collateral to our contract
    # When frac is set - we withdraw a bit less for the same debt fraction
    # f_remove = ((1 + h/2) / (1 + h) * (1 - frac) + frac) * frac
    # where h is health limit.
    # This is less than full h discount but more than no discount
    xy: uint256[2] = AMM.withdraw(user, self._get_f_remove(frac, health_limit))  # [stable, collateral]
```

Observe the formula is selected to reduce nicely when `h=0` or `frac` approaches 0 or 1.

<img width="396" alt="image" src="https://github.com/user-attachments/assets/428404f3-e49b-48a1-926e-107bf367fc77" />

The effect can be observed when plotted, such that `h=0` (blue) reduces to a direct linear relationship between the value of `frac` and `f_remove`, the amount received.

![image](https://github.com/user-attachments/assets/de8bf041-3c55-4095-a848-5330c5c54a6e)

Plotted relative to the case of `h=0`, you see the curve is balanced such as to maximize the liquidation penalty at ~6% when `frac` is set to 0.5 and reducing to no penalty as `frac` approaches 0 or 1.

![image](https://github.com/user-attachments/assets/a816b557-1cc6-40e1-85fd-169f357d5c7e)

When the partial liquidation is complete, the liquidator receives 9.84% of collateral for a 10% liquidation, slightly improving the user's health.

![image](https://github.com/user-attachments/assets/a520e348-f8a8-4b5d-98d0-57c6b634e900)

## HELPFUL LINKS

* [Macket's curvefi/liquidation-demo](https://github.com/curvefi/liquidation-demo)
* [Boa Documentation](https://titanoboa.readthedocs.io/en/latest/api.html)
* [Companion Thread](https://x.com/CurveCap/status/1869361548394959347)
* [YouTube Video](https://youtu.be/UcPmIEMQ5BA)
