# SimpleDEX — Constant Product AMM on Ape Framework

This project implements a simple decentralized exchange (DEX) using a Constant Product Automated Market Maker (CPAMM) in Solidity. It is built using the [Ape Framework](https://docs.apeworx.io/) and uses local and testnet deployments for testing and verification.

---

## Verified Contract

https://sepolia.scrollscan.com//address/0x39ec75440dAe8F8BB39d310dE2F62b13c222fc54#code

## Contracts

### `CPAMM.sol`
A minimal constant product AMM contract that allows:
- Liquidity Provision (`addLiquidity`)
- Liquidity Withdrawal (`removeLiquidity`)
- Swaps (`swapAforB` and `swapBforA`)
- Price Quotes (`getPriceTokenA`, `getPriceTokenB`)

### `TokenA.sol` & `TokenB.sol`
Basic ERC-20 tokens used for testing and liquidity pools.

---

## Installation
- Get an Etherscan API key from [here](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics). This key needs to be added into the environment variables and it's used to publish the contract in the Scroll Sepolia Testnet.
- Install ape in your terminal using `pip install eth-ape`.
- Clone the repo.
- Install plugins & dependencies.

```bash
# Clone the repo
git clone https://github.com/yourname/SimpleDEX.git
cd SimpleDEX

# Install ape
conda create -n ape-env python=3.12 -y
conda activate ape-env
pip install eth-ape

# Install dependencies
ape plugins install .
ape pm install

# add your etherscan api key
export ETHERSCAN_API_KEY=your_key_here
```

---

## Deployment and Verification

### Local Network (e.g. Anvil)

```bash
ape run deploy --network ethereum:local:test
```

### Scroll Sepolia Testnet (L2)

- Found your sepolia testnet [here](https://portal-sepolia.scroll.io/bridge) using Bridge.
- Export your account into `ape`. See [here](https://docs.apeworx.io/ape/stable/userguides/accounts.html#importing-existing-accounts)
- This command will automatically verify your contract

```bash
ape run deploy --sender <ALIAS> --network https://sepolia-rpc.scroll.io
```

---

## Testing

```bash
ape test
```

Tests include:
- Adding/removing liquidity
- Swapping tokens
- Reserve and share accounting
- Price calculations
- Correct deployment of contracts

---

## Verifying on Etherscan

Make sure you have an API key:

```bash
export ETHERSCAN_API_KEY=your_key_here
```

Then run:

```bash
ape run publish --network https://sepolia-rpc.scroll.io
```

---

## Project Structure

```
SimpleDEX/
├── contracts/
│   ├── CPAMM.sol
│   ├── TokenA.sol
│   └── TokenB.sol
├── scripts/
│   └── deploy.py
│   └── publish.py
├── tests/
│   └── test_CPAMM.py
│   └── test_deployment.py
├── ape-config.yaml
└── README.md
```

---

## Resources

- [Ape Framework Docs](https://docs.apeworx.io/)
- [Etherscan API](https://etherscan.io/apis)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)

---

## TODO

- [ ] Add frontend for liquidity and swap
- [ ] Integrate slippage protection
- [ ] Deploy to Base or Polygon
- [ ] Add unit tests for edge cases

---

## License

MIT