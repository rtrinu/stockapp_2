from cryptography.fernet import Fernet, InvalidToken
from backend.core.settings import settings

key = settings.FERNET_KEY
if isinstance(key, str):
    key = key.encode("utf-8")
f = Fernet(key)


def encrypt(secret: str) -> str:
    return f.encrypt(secret.encode("utf-8")).decode("utf-8")


def decrypt(token: str) -> str:
    if not isinstance(token, str):
        raise TypeError(f"decrypt() expects str, got {type(token)}")

    try:
        decrypted = f.decrypt(token.encode("utf-8"))
    except InvalidToken:
        raise ValueError(
            f"Decryption failed: InvalidToken. "
            f"Token length: {len(token)}. Preview: {token[:min(len(token), 10)]}..."
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error during decryption: {e}")

    try:
        return decrypted.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            f"Decrypted bytes could not be decoded as UTF-8. Raw bytes length: {len(decrypted)}, preview: {decrypted[:10]}..."
        )
