import os
from typing import Tuple, Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# --- Algorithmes Classiques ---

def caesar_encrypt(text: str, shift: int) -> str:
    """
    Chiffre un texte avec l'algorithme de César.
    
    > [!WARNING]
    > L'algorithme de César est historiquement significatif mais n'offre aucune 
    > sécurité moderne. Ne l'utilisez pas pour protéger des données sensibles.

    Args:
        text (str): Le texte clair à chiffrer.
        shift (int): Le nombre de décalages (la clé).

    Returns:
        str: Le texte chiffré.
    """
    if not isinstance(text, str) or not isinstance(shift, int):
        raise TypeError("Le texte doit être une chaîne (str) et le décalage un entier (int).")
    
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result

def caesar_decrypt(text: str, shift: int) -> str:
    """
    Déchiffre un texte chiffré avec l'algorithme de César.

    Args:
        text (str): Le texte chiffré.
        shift (int): Le nombre de décalages utilisé pour le chiffrement.

    Returns:
        str: Le texte déchiffré.
    """
    if not isinstance(text, str) or not isinstance(shift, int):
        raise TypeError("Le texte doit être une chaîne (str) et le décalage un entier (int).")
        
    return caesar_encrypt(text, -shift)

def affine_encrypt(text: str, a: int, b: int) -> str:
    """
    Chiffre un texte avec le chiffre Affine (ax + b).
    
    > [!WARNING]
    > Le chiffre Affine n'est pas sécurisé selon les standards modernes.

    Args:
        text (str): Le texte clair à chiffrer.
        a (int): Le coefficient a (doit être premier avec 26).
        b (int): Le décalage b.

    Returns:
        str: Le texte chiffré.
        
    Raises:
        ValueError: Si le coefficient 'a' n'est pas premier avec 26.
    """
    if not isinstance(text, str) or not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Le texte doit être une chaîne et 'a' et 'b' des entiers.")
    
    # Vérification de 'a'
    has_inverse = any((a * i) % 26 == 1 for i in range(26))
    if not has_inverse:
        raise ValueError(f"Le coefficient 'a' ({a}) n'a pas d'inverse modulo 26. Clé invalide.")

    result = ""
    for char in text.upper():
        if char.isalpha():
            p = ord(char) - 65
            c = (a * p + b) % 26
            result += chr(c + 65)
        else:
            result += char
    return result

def affine_decrypt(text: str, a: int, b: int) -> str:
    """
    Déchiffre un texte chiffré avec le chiffre Affine.

    Args:
        text (str): Le texte chiffré.
        a (int): Le coefficient a utilisé pour le chiffrement.
        b (int): Le décalage b utilisé pour le chiffrement.

    Returns:
        str: Le texte clair déchiffré.
        
    Raises:
        ValueError: Si le coefficient 'a' n'a pas d'inverse modulo 26.
    """
    if not isinstance(text, str) or not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Le texte doit être une chaîne et 'a' et 'b' des entiers.")
        
    # Calculer l'inverse de a modulo 26
    a_inv = None
    for i in range(26):
        if (a * i) % 26 == 1:
            a_inv = i
            break
    
    if a_inv is None:
        raise ValueError(f"Le coefficient 'a' ({a}) n'a pas d'inverse modulo 26. Clé invalide.")

    result = ""
    for char in text.upper():
        if char.isalpha():
            c = ord(char) - 65
            p = (a_inv * (c - b)) % 26
            result += chr(p + 65)
        else:
            result += char
    return result

def vigenere_encrypt(text: str, key: str) -> str:
    """
    Chiffre un texte avec le chiffre de Vigenère.
    
    > [!WARNING]
    > Le chiffre de Vigenère est un algorithme classique et ne garantit 
    > aucune sécurité cryptographique moderne.

    Args:
        text (str): Le texte clair à chiffrer.
        key (str): La clé (doit être composée de lettres).

    Returns:
        str: Le texte chiffré.
        
    Raises:
        ValueError: Si la clé est vide ou ne contient pas de lettres.
    """
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("Le texte et la clé doivent être des chaînes (str).")
        
    key = ''.join(filter(str.isalpha, key)).upper()
    if not key:
        raise ValueError("La clé de Vigenère doit contenir au moins une lettre.")
        
    result = ""
    k_len = len(key)
    # L'indice j ne s'incrémente que si un caractère alphabétique est traité
    j = 0 
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[j % k_len]) - 65
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            j += 1
        else:
            result += char
    return result

def vigenere_decrypt(text: str, key: str) -> str:
    """
    Déchiffre un texte chiffré avec le chiffre de Vigenère.

    Args:
        text (str): Le texte chiffré.
        key (str): La clé utilisée pour le chiffrement.

    Returns:
        str: Le texte clair déchiffré.
        
    Raises:
        ValueError: Si la clé est vide ou ne contient pas de lettres.
    """
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("Le texte et la clé doivent être des chaînes (str).")
        
    key = ''.join(filter(str.isalpha, key)).upper()
    if not key:
        raise ValueError("La clé de Vigenère doit contenir au moins une lettre.")
        
    result = ""
    k_len = len(key)
    j = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[j % k_len]) - 65
            result += chr((ord(char) - 65 - shift) % 26 + 65)
            j += 1
        else:
            result += char
    return result

# --- Algorithmes Modernes ---

def generate_rsa_keys() -> Tuple[bytes, bytes]:
    """
    Génère une paire de clés privée et publique RSA (2048 bits).

    Returns:
        Tuple[bytes, bytes]: (clé_privée_pem, clé_publique_pem).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

def rsa_encrypt(message: Union[str, bytes], public_key_pem: bytes) -> bytes:
    """
    Chiffre un message en utilisant une clé publique RSA avec OAEP + SHA256.

    Args:
        message (Union[str, bytes]): Le message à chiffrer.
        public_key_pem (bytes): La clé publique au format PEM.

    Returns:
        bytes: Le message chiffré.
        
    Raises:
        ValueError: Si la clé publique est invalide.
    """
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )
    except Exception as e:
        raise ValueError(f"Clé publique invalide : {str(e)}")
    
    if isinstance(message, str):
        message = message.encode('utf-8')
        
    try:
        ciphertext = public_key.encrypt(
            message,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext
    except ValueError as e:
        raise ValueError(f"Erreur de chiffrement RSA : {str(e)}. Le message est-il trop long ?")

def rsa_decrypt(ciphertext: bytes, private_key_pem: bytes) -> str:
    """
    Déchiffre un message en utilisant une clé privée RSA.

    Args:
        ciphertext (bytes): Le message chiffré.
        private_key_pem (bytes): La clé privée au format PEM.

    Returns:
        str: Le message déchiffré (décodé en UTF-8).
        
    Raises:
        ValueError: Si le déchiffrement échoue ou si la clé privée est invalide.
    """
    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )
    except Exception as e:
        raise ValueError(f"Clé privée invalide : {str(e)}")
    
    try:
        plaintext = private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Échec du déchiffrement RSA : {str(e)}")

def _symmetric_encrypt(text: Union[str, bytes], key: bytes, algorithm_cls, mode_cls=None, block_size: int = 128) -> bytes:
    """Aide générique pour le chiffrement symétrique (AES, DES)."""
    if isinstance(text, str):
        text = text.encode('utf-8')
    
    padder = padding.PKCS7(block_size).padder()
    padded_data = padder.update(text) + padder.finalize()
    
    iv = os.urandom(block_size // 8)
    
    try:
        if mode_cls:
            cipher = Cipher(algorithm_cls(key), mode_cls(iv), backend=default_backend())
        else:
            cipher = Cipher(algorithm_cls(key), modes.CBC(iv), backend=default_backend())
    except ValueError as e:
        raise ValueError(f"Erreur d'initialisation de l'algorithme : {str(e)}. Vérifiez la taille de votre clé.")

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + ciphertext

def _symmetric_decrypt(ciphertext: bytes, key: bytes, algorithm_cls, mode_cls=None, block_size: int = 128) -> str:
    """Aide générique pour le déchiffrement symétrique."""
    iv_len = block_size // 8
    
    if len(ciphertext) <= iv_len:
         raise ValueError(f"Le texte chiffré fourni est trop court. Un IV de {iv_len} octets est requis.")
         
    iv = ciphertext[:iv_len]
    actual_ciphertext = ciphertext[iv_len:]
    
    try:
        if mode_cls:
            cipher = Cipher(algorithm_cls(key), mode_cls(iv), backend=default_backend())
        else:
            cipher = Cipher(algorithm_cls(key), modes.CBC(iv), backend=default_backend())
    except ValueError as e:
        raise ValueError(f"Erreur d'initialisation de l'algorithme : {str(e)}. Vérifiez la taille de votre clé.")
        
    try:
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Déchiffrement échoué : {str(e)}. Mauvaise clé ou données corrompues.")

def aes_encrypt(text: Union[str, bytes], key: bytes) -> bytes:
    """
    Chiffrement AES (mode CBC).

    Args:
        text (Union[str, bytes]): Le texte à chiffrer.
        key (bytes): La clé de chiffrement (16, 24 ou 32 octets).

    Returns:
        bytes: Le texte chiffré préfixé par son vecteur d'initialisation (IV).
        
    Raises:
        ValueError: Si la longueur de la clé n'est pas correcte (16, 24 ou 32 octets).
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"La clé AES doit être de 16, 24 ou 32 octets, mais est de {len(key)} octets.")
    return _symmetric_encrypt(text, key, algorithms.AES, modes.CBC, block_size=128)

def aes_decrypt(ciphertext: bytes, key: bytes) -> str:
    """
    Déchiffrement AES (mode CBC).

    Args:
        ciphertext (bytes): Le texte chiffré incluant l'IV au début.
        key (bytes): La clé de déchiffrement (16, 24 ou 32 octets).

    Returns:
        str: Le texte clair déchiffré.
        
    Raises:
        ValueError: Si la longueur de la clé est incorrecte ou si le déchiffrement échoue.
    """
    if len(key) not in (16, 24, 32):
        raise ValueError(f"La clé AES doit être de 16, 24 ou 32 octets, mais est de {len(key)} octets.")
    return _symmetric_decrypt(ciphertext, key, algorithms.AES, modes.CBC, block_size=128)

def des_encrypt(text: Union[str, bytes], key: bytes) -> bytes:
    """
    Chiffrement DES (implémenté via TripleDES pour une meilleure fiabilité).
    
    > [!WARNING]
    > L'algorithme DES / 3DES est considéré comme obsolète et faible face 
    > aux attaques par force brute. Utilisez plutôt AES pour un projet réel.

    Args:
        text (Union[str, bytes]): Le texte à chiffrer.
        key (bytes): La clé de chiffrement (doit être exactement 8, 16 ou 24 octets pour 3DES).

    Returns:
        bytes: Le texte chiffré préfixé par l'IV.
        
    Raises:
        ValueError: Si la longueur de la clé est incorrecte.
    """
    if len(key) not in (8, 16, 24):
         raise ValueError(f"La clé DES (TripleDES) doit être de 8, 16 ou 24 octets, mais est de {len(key)} octets.")
    return _symmetric_encrypt(text, key, algorithms.TripleDES, modes.CBC, block_size=64)

def des_decrypt(ciphertext: bytes, key: bytes) -> str:
    """
    Déchiffrement DES (TripleDES).

    Args:
        ciphertext (bytes): Le texte chiffré incluant l'IV au début.
        key (bytes): La clé de déchiffrement.

    Returns:
        str: Le texte clair.
        
    Raises:
        ValueError: Si la longueur de la clé est incorrecte ou si le déchiffrement échoue.
    """
    if len(key) not in (8, 16, 24):
         raise ValueError(f"La clé DES (TripleDES) doit être de 8, 16 ou 24 octets, mais est de {len(key)} octets.")
    return _symmetric_decrypt(ciphertext, key, algorithms.TripleDES, modes.CBC, block_size=64)
