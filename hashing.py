import os
import hashlib
import hmac
from typing import Tuple


def _pbkdf2(password: str, salt: bytes, iterations: int = 200_000, dklen: int = 32) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=dklen)


def hash_password(password: str) -> str:
    """Return a string "pbkdf2_sha256$iterations$salt_hex$hash_hex"."""
    iterations = 200_000
    salt = os.urandom(16)
    dk = _pbkdf2(password, salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iter_s, salt_hex, hash_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iter_s)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        candidate = _pbkdf2(password, salt, iterations, dklen=len(expected))
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False


def generate_hash(data: str) -> str:
    """Simple SHA-256 hash for transaction integrity and signatures."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
