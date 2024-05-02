import json
from web3 import Web3
from flask import Flask, request, jsonify
from dict2 import abi_paths, contract_addresses
from security.encryption import aes_encrypt, aes_decrypt
from security.access import authenticate_user
from security.pipeline import blockchain_connection

app = Flask(__name__)

def load_all_contracts():
    web3 = blockchain_connection()
    if not web3 or not web3.is_connected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    contracts = {}
    for name, abi_path in abi_paths.items():
        try:
            with open(abi_path, 'r') as file:
                abi = json.load(file)
        except FileNotFoundError:
            print(f"ABI file at {abi_path} not found for contract {name}. Skipping.")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding ABI file at {abi_path} for contract {name}. Ensure it is valid JSON. Skipping.")
            continue
        
        contract_address = contract_addresses.get(name)
        if contract_address:
            contracts[name] = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        else:
            print(f"Address not found for contract {name}. Skipping.")
    
    return contracts

contracts = load_all_contracts()
if contracts:
    for name, contract in contracts.items():
        print(f"Contract '{name}' loaded successfully.")
else:
    print("No contracts loaded.")

@app.route('/api/send_transaction', methods=['POST'])
def handle_transaction():
    data = request.json
    contract_name = data['contract_name']
    function_name = data['function_name']
    user_address = data['user_address']
    encrypted_private_key = data['encrypted_private_key']
    value = data.get('value', 0)

    contract = contracts.get(contract_name)
    if not contract:
        return jsonify({'error': f'Contract {contract_name} not found'}), 404

    function = getattr(contract.functions, function_name, None)
    if not function:
        return jsonify({'error': f'Function {function_name} not found in contract {contract_name}'}), 404

    txn_hash = send_transaction(function, user_address, encrypted_private_key, value)
    if txn_hash:
        return jsonify({'txn_hash': txn_hash})
    else:
        return jsonify({'error': 'Failed to send transaction'}), 500

def send_transaction(contract_function, user_address, encrypted_private_key, value=0):
    web3 = blockchain_connection()
    if not web3 or not web3.is_connected():
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
        
        private_key = aes_decrypt(encrypted_private_key)

        signed_txn = web3.eth.account.signTransaction(txn, private_key)
        encrypted_txn_hash = aes_encrypt(signed_txn.rawTransaction)
        
        return encrypted_txn_hash
    except Exception as e:
        print(f"Failed to send transaction: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
