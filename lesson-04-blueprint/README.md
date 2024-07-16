# Lesson 4: Blueprint

## [🎥 Curve Titanoboa Tutorial Video 4 : Blueprint 🎬](https://youtu.be/yeNtQvO20ag)

For our final prerequisite lesson before we get into arb trading, we create a test loan and a healthy Curve liquidity pool to ensure smooth liquidations.

To do so, we often need to interact with contracts that are not yet verified on Etherscan (or in this case, Arbiscan).  Curve factories help devs in this process by providing verified implementation contracts.  In this lesson we show how to use Titanoboa to quickly reuse these ABIs to load contracts.

We also introduce Titanoboa's `prank` function, which allows you to spoof calls from any address


### ABI CONTRACT FACTORY
This Titanoboa object represents an ABI contract that has not been coupled with an address yet.
This is named `Factory` instead of `Deployer` because it doesn't actually do any contract deployment.

`existing_contract = ABIContractFactory.from_abi_dict(abi, name=name).at(addr)`

### PRANK 

A context manager which temporarily sets eoa and resets it on exit.

```
>>> import boa
>>> boa.env.eoa
'0x0000000000000000000000000000000000000065'

>>> with boa.env.prank("0x00000000000000000000000000000000000000ff"):
...    boa.env.eoa
...
'0x00000000000000000000000000000000000000ff'

>>> boa.env.eoa
'0x0000000000000000000000000000000000000065'
```


## HELPFUL LINKS

**Contracts**
* [Curve Llama Lend Factory](https://arbiscan.io/address/0xcaEC110C784c9DF37240a8Ce096D352A75922DeA)
* [Arbitrum crvUSD Proxy](https://arbiscan.io/address/0x498Bf2B1e120FeD3ad3D42EA2165E9b73f99C1e5#code)
* [Arbitrum L2GatewayToken.sol](https://github.com/OffchainLabs/token-bridge-contracts/blob/main/contracts/tokenbridge/libraries/L2GatewayToken.sol)

**Documentation**
* [Arbitrum ERC20 Token Bridging](https://docs.arbitrum.io/build-decentralized-apps/token-bridging/token-bridge-erc20)
* [Titanoboa prank function](https://titanoboa.readthedocs.io/en/latest/api.html#boa.environment.Env.prank)
* [Vyper Built-In Functions](https://docs.vyperlang.org/en/stable/built-in-functions.html#chain-interaction)

