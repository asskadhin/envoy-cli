"""Tests for envoy_cli.crypto encryption/decryption utilities."""

import pytest
from envoy_cli.crypto import encrypt, decrypt


PASSWORD = "super-secret-passphrase"
PLAINTEXT = "DB_PASSWORD=hunter2\nAPI_KEY=abc123"


def test_encrypt_returns_string():
    result = encrypt(PLAINTEXT, PASSWORD)
    assert isinstance(result, str)
    assert result != PLAINTEXT


def test_decrypt_roundtrip():
    payload = encrypt(PLAINTEXT, PASSWORD)
    recovered = decrypt(payload, PASSWORD)
    assert recovered == PLAINTEXT


def test_encrypt_produces_unique_ciphertexts():
    """Each encryption call should produce a different ciphertext (random salt)."""
    payload1 = encrypt(PLAINTEXT, PASSWORD)
    payload2 = encrypt(PLAINTEXT, PASSWORD)
    assert payload1 != payload2


def test_decrypt_with_wrong_password_raises():
    payload = encrypt(PLAINTEXT, PASSWORD)
    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt(payload, "wrong-password")


def test_decrypt_with_corrupted_payload_raises():
    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt("not-valid-base64-payload!!", PASSWORD)


def test_encrypt_empty_string():
    payload = encrypt("", PASSWORD)
    assert decrypt(payload, PASSWORD) == ""


def test_encrypt_multiline_content():
    content = "\n".join(f"KEY_{i}=value_{i}" for i in range(50))
    payload = encrypt(content, PASSWORD)
    assert decrypt(payload, PASSWORD) == content
