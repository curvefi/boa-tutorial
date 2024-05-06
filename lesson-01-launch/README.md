# Lesson 1: Launch

## [🎥 Curve Titanoboa Tutorial Video 1 : Launch 🎬](https://youtu.be/_tqBRPZOvfM)

The Curve Titanoboa Tutorial covers the management of a memecoin on [Curve's permissionless Llama Lend markets](https://lend.curve.fi/).

This lesson shows how to quickly install Titanoboa and quickly deploy a memecoin to Sepolia.

## Boa Installation

Installing Titanoboa from [PyPI](https://pypi.org/project/titanoboa/)

```
pip install titanoboa
```

The latest in-development version of Titanoboa can be [installed from GitHub](https://github.com/vyperlang/titanoboa)

```
pip install git+https://github.com/vyperlang/titanoboa
```

## Other Installation Notes

The video launches boa within a Jupyter Notebook in a virtual environment on the local machine.  

To create a virtual environment:

```
virtualenv boa-env
source boa-env/bin/activate
```

Other librarires installed into the virtual environment

```
pip install jupyter
pip install snekmate
```

## ERC-20 Token Launch

The ERC20 token launch script in this case is courtesy [Charles Cooper](https://github.com/charles-cooper) via [try.vyperlang.org](https://try.vyperlang.org/hub/user-redirect/lab/tree/shared/charles-cooper/demo-token.ipynb)

```
!pip install -q "git+https://github.com/pcaversaccio/snekmate@modules"
import boa
boa.set_browser_env()
boa.env.set_chain_id(0xaa36a7)  # sepolia
from snekmate.tokens import ERC20
my_token = ERC20.deploy("Vyper wif hat", "VWIF", 100_000_000, "", "")
```

The token is sourced from the [snekmate default ERC-20 implementation](https://github.com/pcaversaccio/snekmate/blob/main/src/snekmate/tokens/ERC20.vy) from [snekmate](https://github.com/pcaversaccio/snekmate) by [pcaversaccio](https://github.com/pcaversaccio)

## Helpful Links

**Github**

* [Snekmate](https://github.com/pcaversaccio/snekmate)
* [Jupyter](https://github.com/jupyter)
* [pytest](https://github.com/pytest-dev/pytest)

**Other**
* [Sepolia Etherscan](https://sepolia.etherscan.io/tx/0x2a126c7a7320603167a8baf2977f95e320ec175e77f5947271eb0e17022860cc)
* [Try Vyper](https://try.vyperlang.org/hub/user-redirect/lab/tree/shared/zcor/boa-tutorial)

For more details, consult the **Curve Vyper Tutorial:**

 * [GitHub](https://github.com/curvefi/vyper-tutorial)
 * [YouTube](https://www.youtube.com/playlist?list=PLVOHzVzbg7bFnLnl3t5egG5oWpOhfdD1D) 
