import json
from web3 import Web3
from pipeline import blockchain_connection

abi_path = 'C:\\Users\\haoha\\OneDrive\\Desktop\\personal\\Projects\\Hackathons\\hacksingapore 2024\\DeFi P2P Lending\\contract\\abi.json'
def load_contract(abi_path, contract_address):
    # Try to establish a blockchain connection
    web3 = blockchain_connection()
    if not web3 or not web3.is_connected():
        print("Failed to connect to the Ethereum network.")
        return None
    
    # Load the Application binary Interface (ABI)
    try:
        with open(abi_path, 'r') as file:
            abi = json.load(file)
    except FileNotFoundError:
        print("ABI file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding ABI file. Ensure it is valid JSON.")
        return None

    return web3.eth.contract(address=contract_address, abi=abi)

contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'
contract = load_contract(abi_path, contract_address)

#interact with contract
def get_loan_status(user_address):
    if contract:
        try:
            return contract.functions.getLoanStatus(user_address).call()
        except Exception as e:
            print(f"Failed to retrieve loan status: {e}")
    return "Contract is not available."

def submit_transaction(user_address, amount):
    if contract:
        try:
            txn_dict = {
                'from': user_address,
                'value': Web3.toWei(amount, 'ether'),
                'gas': 2000000
            }
            # private key
            return "Transaction would be sent here."
        except Exception as e:
            print(f"Failed to submit transaction: {e}")
    return "Contract is not available."