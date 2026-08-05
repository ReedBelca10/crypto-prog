import pytest
from crypto_utils import (
    caesar_encrypt, caesar_decrypt,
    affine_encrypt, affine_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    generate_rsa_keys, rsa_encrypt, rsa_decrypt,
    aes_encrypt, aes_decrypt,
    des_encrypt, des_decrypt
)

# --- Caesar Tests ---

def test_caesar_encrypt_basic():
    assert caesar_encrypt("BONJOUR", 3) == "ERQMRXU"

def test_caesar_decrypt_basic():
    assert caesar_decrypt("ERQMRXU", 3) == "BONJOUR"

def test_caesar_wrap_around():
    assert caesar_encrypt("XYZ", 5) == "CDE"
    assert caesar_decrypt("CDE", 5) == "XYZ"

def test_caesar_non_alpha():
    assert caesar_encrypt("HELLO WORLD! 123", 1) == "IFMMP XPSME! 123"

def test_caesar_empty_string():
    assert caesar_encrypt("", 5) == ""

def test_caesar_invalid_types():
    with pytest.raises(TypeError):
        caesar_encrypt(123, 5) # type: ignore
    with pytest.raises(TypeError):
        caesar_encrypt("TEST", "5") # type: ignore

# --- Affine Tests ---

def test_affine_encrypt_valid():
    assert affine_encrypt("BONJOUR", 5, 8) == "NAVBAEP"

def test_affine_decrypt_valid():
    assert affine_decrypt("NAVBAEP", 5, 8) == "BONJOUR"

def test_affine_invalid_a():
    with pytest.raises(ValueError, match="n'a pas d'inverse modulo 26"):
        affine_encrypt("TEST", 2, 5)  # 2 is not coprime with 26
    with pytest.raises(ValueError, match="n'a pas d'inverse modulo 26"):
        affine_decrypt("TEST", 13, 5) # 13 is not coprime with 26

def test_affine_non_alpha():
    assert affine_encrypt("TEST 123!", 5, 8) == "ZCUZ 123!"

# --- Vigenere Tests ---

def test_vigenere_encrypt_valid():
    assert vigenere_encrypt("BONJOUR", "CLE") == "DZRLZYT"

def test_vigenere_decrypt_valid():
    assert vigenere_decrypt("DZRLZYT", "CLE") == "BONJOUR"

def test_vigenere_non_alpha_key():
    # Only letters from the key are used
    assert vigenere_encrypt("BONJOUR", "CL123E") == "DZRLZYT"

def test_vigenere_empty_key():
    with pytest.raises(ValueError, match="doit contenir au moins une lettre"):
        vigenere_encrypt("BONJOUR", "123!@#")
    with pytest.raises(ValueError, match="doit contenir au moins une lettre"):
        vigenere_encrypt("BONJOUR", "")

# --- RSA Tests ---

def test_rsa_key_generation():
    priv, pub = generate_rsa_keys()
    assert isinstance(priv, bytes)
    assert isinstance(pub, bytes)
    assert b"PRIVATE KEY" in priv
    assert b"PUBLIC KEY" in pub

def test_rsa_encrypt_decrypt():
    priv, pub = generate_rsa_keys()
    message = "Secret message 123!"
    ciphertext = rsa_encrypt(message, pub)
    assert ciphertext != message.encode('utf-8')
    plaintext = rsa_decrypt(ciphertext, priv)
    assert plaintext == message

def test_rsa_invalid_public_key():
    with pytest.raises(ValueError, match="Clé publique invalide"):
        rsa_encrypt("Test", b"not a key")

def test_rsa_invalid_private_key():
    with pytest.raises(ValueError, match="Clé privée invalide"):
        rsa_decrypt(b"some ciphertext", b"not a key")

# --- AES Tests ---

def test_aes_encrypt_decrypt():
    key = b"0123456789abcdef"  # 16 bytes
    message = "Super secret AES message."
    ciphertext = aes_encrypt(message, key)
    assert ciphertext != message.encode('utf-8')
    plaintext = aes_decrypt(ciphertext, key)
    assert plaintext == message

def test_aes_invalid_key_length():
    with pytest.raises(ValueError, match="doit être de 16, 24 ou 32 octets"):
        aes_encrypt("Test", b"short")
    with pytest.raises(ValueError, match="doit être de 16, 24 ou 32 octets"):
        aes_decrypt(b"ciphertext", b"too_long_key_that_is_invalid_len_123")

# --- DES Tests ---

def test_des_encrypt_decrypt():
    key = b"12345678"  # 8 bytes
    message = "DES test message"
    ciphertext = des_encrypt(message, key)
    assert ciphertext != message.encode('utf-8')
    plaintext = des_decrypt(ciphertext, key)
    assert plaintext == message

def test_des_invalid_key_length():
    with pytest.raises(ValueError, match="doit être de 8, 16 ou 24 octets"):
        des_encrypt("Test", b"short")
    with pytest.raises(ValueError, match="doit être de 8, 16 ou 24 octets"):
        des_decrypt(b"ciphertext", b"12345")
