# Lesson 2: Fork

## [🎥 Curve Titanoboa Tutorial Video 2 : Fork 🎬](https://youtu.be/AkYMDVmcaYw)

This lesson shows how to fork a live RPC and read from a contract.


### FORK

To fork an RPC node

```
boa.env.fork(RPC_URL)
```

### LOAD CONTRACT FROM BLOCK EXPLORER

Read a contract from a block explorer

```
boa.from_etherscan(
    address: Any,
    name=None,
    uri='https://api.etherscan.io/api',
    api_key=None,
)
```

### INSTALL PYENV (optional)

To install pyenv for managing environment variables

`pip install python-dotenv`

## HELPFUL LINKS

**Llama Lend One Way Lending Factory**
* [Arbiscan](https://arbiscan.io/address/0xcaec110c784c9df37240a8ce096d352a75922dea)
* [Github](https://github.com/curvefi/curve-stablecoin/blob/master/contracts/lending/OneWayLendingFactory.vy)

**Misc**

* [Arbiscan](https://arbiscan.io/)
* [Alchemy](https://www.alchemy.com/)
* [Titanoboa Documentation](https://titanoboa.readthedocs.io/)
* [Titanoboa Source](https://github.com/vyperlang/titanoboa/)
* [Try Vyper](https://try.vyperlang.org/hub/user-redirect/lab/tree/shared/zcor/boa-tutorial)
