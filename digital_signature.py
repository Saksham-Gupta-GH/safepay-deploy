from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

def sign_data(data):
    return private_key.sign(data.encode(), padding.PKCS1v15(), hashes.SHA256())

def verify_signature(data, signature):
    try:
        public_key.verify(signature, data.encode(), padding.PKCS1v15(), hashes.SHA256())
        return True
    except:
        return False
