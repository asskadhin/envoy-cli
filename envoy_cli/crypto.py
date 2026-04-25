"""Encryption and decryption utilities for .env file secrets."""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16
ITERATIONS = 390000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt(plaintext: str, password: str) -> str:
    """Encrypt plaintext using a password.

    Returns a base64-encoded string containing the salt and ciphertext.
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(plaintext.encode())
    payload = base64.urlsafe_b64encode(salt + ciphertext)
    return payload.decode()


def decrypt(payload: str, password: str) -> str:
    """Decrypt a payload produced by :func:`encrypt`.

    Raises:
        ValueError: If decryption fails (wrong password or corrupted data).
    """
    try:
        raw = base64.urlsafe_b64decode(payload.encode())
        salt = raw[:SALT_SIZE]
        ciphertext = raw[SALT_SIZE:]
        key = derive_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(ciphertext).decode()
    except Exception as exc:
        raise ValueError("Decryption failed: invalid password or corrupted data.") from exc
