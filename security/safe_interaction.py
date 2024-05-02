from web3 import Web3
import json
from pipeline import blockchain_connection
from encryption import aes_encrypt, aes_decrypt

def secure_load_contract(abi_path, contract_address, encryption_key=None):
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

    contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    

    if encryption_key:
        contract.bytecode = aes_decrypt(contract.bytecode, encryption_key)
    
    return contract

def secure_send_transaction(contract_function, user_address, private_key, value=0, encryption_key=None):
    web3 = blockchain_connection()
    if not web3 or not web3.isConnected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    try:
        txn_dict = {
            'from': user_address,
            'value': Web3.toWei(value, 'ether'),
            'gas': 2000000,
            'nonce': web3.eth.getTransactionCount(user_address)
        }
        txn = contract_function.buildTransaction(txn_dict)
        
        # Encrypt transaction data if encryption key is provided
        if encryption_key:
            txn = aes_encrypt(json.dumps(txn), encryption_key)
        
        signed_txn = web3.eth.account.signTransaction(txn, private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return web3.toHex(txn_hash)
    except Exception as e:
        print(f"Failed to send transaction: {e}")
    return "Failed to send transaction."
