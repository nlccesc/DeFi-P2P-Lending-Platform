from Crypto.Cipher import AES
import base64
from errors import DecryptionError
import logging

def aes_decrypt(encrypted_data, key):
    """ Decrypt data using AES-256 GCM. """
    decoded_data = base64.b64decode(encrypted_data)
    nonce = decoded_data[:16]
    tag = decoded_data[16:32]
    ciphertext = decoded_data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        logging.info("Data decrypted")
        return decrypted_data.decode()
    except ValueError as e:
        logging.error("Decryption failure - Data might be tampered or key incorrect")
        raise DecryptionError("Invalid decryption - Data might be tampered or key incorrect.") from e
