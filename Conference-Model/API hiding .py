from cryptography.fernet import Fernet
import base64
import os
import getpass
import hashlib

# Function to generate a key from a password
def generate_key(password):
    # Derive a key from the password
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

# Function to encrypt the API key
def encrypt_api_key(api_key, password):
    key = generate_key(password)
    f = Fernet(key[:688])  
    encrypted_key = f.encrypt(api_key.encode())
    return encrypted_key

# Function to decrypt the API key
def decrypt_api_key(encrypted_key, password):
    key = generate_key(password)
    f = Fernet(key[:688])  
    decrypted_key = f.decrypt(encrypted_key).decode()
    return decrypted_key

# Example usage
if __name__ == "__main__":
    api_key = '' #PLACE API CODE HERE
    password = getpass.getpass("Enter password to encrypt the API key: ")
    
    # Encrypt the API key
    encrypted_key = encrypt_api_key(api_key, password)
    print("Encrypted API Key:", encrypted_key)

    # Decrypt the API key (for demonstration, you can ask for the password)
    password_for_decrypt = getpass.getpass("Enter password to decrypt the API key: ")
    try:
        decrypted_key = decrypt_api_key(encrypted_key, password_for_decrypt)
        print("Decrypted API Key:", decrypted_key)
    except Exception as e:
        print("Failed to decrypt the API key:", str(e))