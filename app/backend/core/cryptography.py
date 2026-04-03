from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


def encrypt(secret: str) -> str:
    return f.encrypt(secret.encode("utf-8")).decode("utf-8")


def decrypt(token: str) -> str:
    return f.decrypt(token.encode("utf-8")).decode("utf-8")
