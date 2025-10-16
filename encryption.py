import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac


KEY_PATH = os.path.join(os.path.dirname(__file__), "aes_key.bin")


def _load_or_create_key() -> bytes:
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            key = f.read()
        if len(key) == 32:
            return key
    key = os.urandom(32)
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key


_KEY = _load_or_create_key()


def encrypt_data(data: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(_KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data.encode("utf-8")) + padder.finalize()
    ct = encryptor.update(padded) + encryptor.finalize()
    # Compute HMAC over iv || ct
    h = hmac.HMAC(_KEY, hashes.SHA256())
    h.update(iv + ct)
    tag = h.finalize()
    return base64.b64encode(iv + ct + tag).decode("ascii")


def decrypt_data(token: str) -> str:
    raw = base64.b64decode(token.encode("ascii"))
    iv, rest = raw[:16], raw[16:]
    ct, tag = rest[:-32], rest[-32:]
    # Verify HMAC
    h = hmac.HMAC(_KEY, hashes.SHA256())
    h.update(iv + ct)
    h.verify(tag)
    cipher = Cipher(algorithms.AES(_KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    pt = unpadder.update(padded) + unpadder.finalize()
    return pt.decode("utf-8")
