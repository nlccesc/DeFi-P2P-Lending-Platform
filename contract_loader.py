import json
from web3 import Web3
from security.pipeline import blockchain_connection
import dict2
from dict2 import abi_paths, contract_addresses

def load_contract(abi_path, contract_address):
    web3 = blockchain_connection()
    if not web3 or not web3.is_connected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    try:
        with open(abi_path, 'r') as file:
            abi = json.load(file)
    except FileNotFoundError:
        print(f"ABI file at {abi_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding ABI file at {abi_path}. Ensure it is valid JSON.")
        return None

    return web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
