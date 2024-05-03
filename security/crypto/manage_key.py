from Crypto.Random import get_random_bytes
import logging

logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def generate_aes_key():

    key = get_random_bytes(32)
    logging.info("AES key generated.")
    return key

# can add in functions for key rotation and Key mngmt services or hardware security module interfacing