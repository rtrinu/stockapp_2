from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


def encrypt(token) -> bytes:
    encrypted_token = f.encrypt(token.encode())
    return encrypted_token


def decrypt(token) -> bytes:
    decrypted_token = f.decrypt(token.decode())
    return decrypted_token
