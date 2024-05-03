from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def generate_aes_key():
    return get_random_bytes(32)

def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def aes_decrypt(encrypted_data, key):
    decoded_data = base64.b64decode(encrypted_data)
    nonce = decoded_data[:16]
    tag = decoded_data[16:32]
    ciphertext = decoded_data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode()
    except ValueError:
        raise Exception("Invalid Encryption.")
