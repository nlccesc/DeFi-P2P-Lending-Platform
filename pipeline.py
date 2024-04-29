from web3 import Web3

def blockchain_connection():
    try:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e716b1fec5d34560a1e3f8906b3d9642'))
        if w3.is_connected:
            print("Connected to the ETH blockchain.")
        else:
            print("Failed to connect to the ETH blockchain.")
        return w3
    except Exception as e:
        print(f"An error has occured: {str(e)}")
        return None

blockchain_connection()
