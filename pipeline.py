from web3 import Web3

def blockchain_connection():
    w3 = Web3(Web3.HTTPProvider('http://mainnet.infura.io/v3/project_id'))
    if w3.is_connected:
        print("Connected to the ETH blockchain.")
    else:
        print("Failed to connect to the ETH blockchain.")
    return w3