from crypto.encryption import aes_encrypt
from crypto.decryption import aes_decrypt
from manage_key import generate_aes_key

# Example usage
if __name__ == "__main__":
    key = generate_aes_key()
    encrypted_data, key = aes_encrypt("Hello, world!", key) # example
    print("Encrypted:", encrypted_data)
    try:
        decrypted_data = aes_decrypt(encrypted_data, key)
        print("Decrypted:", decrypted_data)
    except Exception as e:
        print("Error:", str(e))
