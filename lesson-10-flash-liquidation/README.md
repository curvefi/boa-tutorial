# Lesson 10: Flash Liquidation

## [🎥 Curve Titanoboa Tutorial Video 10 : Flash Liquidation 🎬](https://youtu.be/LeTE3Blx-W0)

Curve leaves $1 million in the FlashLender contract.  Anybody can use it to make money, provided they repay the loan in the same block.  This unit shows off how to use the FlashLender to perform liquidations on Llama Lend.

The lesson returns to the fictitious VyperWif token introduced in the first six lessons.  A borrower is put into a liquidation state:

<img width="1393" alt="image" src="https://github.com/user-attachments/assets/35781fa2-47ef-4a00-8893-23e456dc6f7d" />

A [liquidator contract](liquidator.vy) is deployed to handle the flash loan, which takes the $1MM from the FlashLender to trade through the liquidity pool and perform a liquidation.

### ERC-3156

The ERC-3156 specifies standard interfaces and processes for single asset flash loans.
The receiving contract must have an `onFlashLoan` function to handle the loan.
The lending contract must include the following functions:

* maxFlashLoan: The amount of currency available to be lent.
* flashFee: The fee to be charged for a given loan.
* flashLoan: Initiate a flash loan, which calls the onFlashLoan contract.

### ERC-3156 BYTES CALLDATA

The ERC-3156 standard includes a bytes calldata data parameter in the onFlashLoan bunction.
This optional parameter allows caller to pass arbitrary information to the receiver.


## HELPFUL LINKS

* [crvUSD FlashLender](https://etherscan.io/address/0xa7a4bb50af91f90b6feb3388e7f8286af45b299b#code)
* [Boa Documentation](https://titanoboa.readthedocs.io/)
* [Companion Thread](https://x.com/CurveCap/status/1883874709038903362)
