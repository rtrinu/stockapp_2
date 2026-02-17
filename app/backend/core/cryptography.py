from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


def encrypt(secret: str) -> str:
    if not isinstance(secret, str):
        raise TypeError("encrypt() expects str")
    token_bytes = secret.encode("utf-8")
    encrypted_bytes = f.encrypt(token_bytes)
    return encrypted_bytes.decode("utf-8")


def decrypt(token) -> bytes:
    decrypted_token = f.decrypt(token.decode())
    return decrypted_token
