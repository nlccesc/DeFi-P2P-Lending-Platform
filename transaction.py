from web3 import Web3
from security.pipeline import blockchain_connection

def send_transaction(contract_function, user_address, private_key, value=0):
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
        signed_txn = web3.eth.account.signTransaction(txn, private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return web3.toHex(txn_hash)
    except Exception as e:
        print(f"Failed to send transaction: {e}")
    return "Failed to send transaction."
