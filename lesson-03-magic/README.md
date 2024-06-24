# Lesson 3: Magic

## [🎥 Curve Titanoboa Tutorial Video 3 : Magic 🎬](https://youtu.be/yf5gbd4sK2c)

This lesson shows off the `%%vyper` cell magic command that compiles a dummy Vyper price oracle contract into a variable for testing Curve Llama Lend.


### VIEW MAGIC COMMANDS

Built-in IPython magic command to list all currently available magic functions

`%lsmagic`

### LOAD CONTRACT FROM BLOCK EXPLORER

The EOA (Externally Owned Account) is the account Titanoboa uses by default for `msg.sender` top-level calls and `tx.origin` in state-mutating function calls

`boa.env.eoa`


## HELPFUL LINKS

**Vyper Code**
* [DummyPriceOracle.vy](https://github.com/curvefi/curve-stablecoin/blob/master/contracts/testing/DummyPriceOracle.vy)

**Documentation**
* [IPython](https://ipython.readthedocs.io/)
* [Curve Oracles](https://curve.readthedocs.io/factory-oracles.html)
* [Boa IPython Cells](https://titanoboa.readthedocs.io/en/latest/testing.html#ipython-vyper-cells)
