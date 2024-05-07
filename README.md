# DeFi (Backend)

The backend project.

## Project Structure

### `abi` folder

This folder contains the Application Binary Interface (ABI) files for this idea. These files are needed for the interaction between binary program modules where it specifies data type, size, alignment, etc. These ABIs allow the encoding and decoding of data to and from smart contracts.

Contents: ABI files for disbursement, interest calculation, loan agreement, repayment, and an overall smart contract.

### `contract` folder

This folder contains the solidity files (`.sol`) which is used for developing smart contracts that run on the Ethereum Virtual Machine (EVM). This allows for a clear record of transactions. These contracts are done to facilitate the loan agreement, repayment, etc.

### `dict.py` file

Some test cases.

### `dict2.py` file

Some definitions that is used in `interaction.py`.

### `interface.py` file

Interacts with ETH smart contracts using the `web3.py` library. This basically loads and interact with the smart contracts that make the platform.