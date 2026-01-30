from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_pwd(pwd: str) -> str:
    hashed = password_hash.hash(pwd)
    return hashed


def verify_pwd(pwd: str, hashed) -> bool:
    is_valid = password_hash.verify(pwd, hashed)
    return is_valid
