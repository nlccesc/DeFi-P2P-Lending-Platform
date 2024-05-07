import base64
import logging

from Crypto.Cipher import AES

from security.crypto.manage_key import generate_aes_key


def aes_encrypt(data, key=None):

    if key is None:
        key = generate_aes_key()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    encrypted_data = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    logging.info("Data encrypted")
    return encrypted_data, key