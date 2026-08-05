"""
Module CLI pour l'outil de cryptographie.

Fournit une interface en ligne de commande pour chiffrer et déchiffrer
du texte avec divers algorithmes classiques et modernes.

Usage:
    python crypto_cli.py <methode> <action> [texte] [options]

Tested on: Python 3.10+
"""
import argparse
import hashlib
import sys
import os
from typing import Optional

import crypto_utils


def _read_content(text_arg: Optional[str]) -> Optional[str]:
    """
    Lit le contenu à partir de l'argument texte ou d'un chemin de fichier.

    Si ``text_arg`` est le chemin d'un fichier existant, son contenu est
    lu et renvoyé. Sinon, ``text_arg`` est renvoyé tel quel.

    Args:
        text_arg: Le texte brut ou le chemin d'un fichier.

    Returns:
        Le contenu textuel, ou ``None`` si ``text_arg`` est ``None``.
    """
    if text_arg is None:
        return None

    if os.path.isfile(text_arg):
        try:
            with open(text_arg, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            print(f"Erreur: Impossible de lire le fichier '{text_arg}': {e}", file=sys.stderr)
            sys.exit(1)

    return text_arg


def _prepare_aes_key(key_str: str) -> bytes:
    """
    Prépare une clé AES à partir d'une chaîne utilisateur.

    Si la longueur de la clé encodée en UTF-8 n'est pas 16, 24 ou 32
    octets, un hachage SHA-256 est utilisé pour obtenir une clé de 32 octets.

    Args:
        key_str: La clé fournie par l'utilisateur.

    Returns:
        La clé sous forme de bytes, prête pour AES.
    """
    key_bytes = key_str.encode("utf-8")
    if len(key_bytes) not in (16, 24, 32):
        key_bytes = hashlib.sha256(key_bytes).digest()  # 32 bytes
    return key_bytes


def _prepare_des_key(key_str: str) -> bytes:
    """
    Prépare une clé DES/3DES à partir d'une chaîne utilisateur.

    Si la longueur de la clé encodée en UTF-8 n'est pas exactement 8
    octets, un hachage SHA-256 est tronqué à 24 octets (TripleDES).

    Args:
        key_str: La clé fournie par l'utilisateur.

    Returns:
        La clé sous forme de bytes, prête pour TripleDES.
    """
    key_bytes = key_str.encode("utf-8")
    if len(key_bytes) != 8:
        key_bytes = hashlib.sha256(key_bytes).digest()[:24]
    return key_bytes


def _hex_to_bytes(hex_str: str, algo_name: str) -> bytes:
    """
    Convertit une chaîne hexadécimale en bytes.

    Args:
        hex_str: La chaîne hexadécimale.
        algo_name: Le nom de l'algorithme (pour les messages d'erreur).

    Returns:
        Les bytes correspondants.

    Raises:
        SystemExit: Si la chaîne n'est pas un hexadécimal valide.
    """
    try:
        return bytes.fromhex(hex_str)
    except ValueError:
        print(
            f"Erreur: Pour le déchiffrement {algo_name}, le texte d'entrée "
            "doit être une chaîne hexadécimale.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> None:
    """Point d'entrée principal de l'interface en ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Crypto CLI (César, Affine, Vigenère, RSA, DES, AES)"
    )
    parser.add_argument(
        "method",
        choices=["caesar", "affine", "vigenere", "rsa", "des", "aes"],
        help="Méthode de chiffrement",
    )
    parser.add_argument(
        "action",
        choices=["encrypt", "decrypt", "generate-keys"],
        help="Action à effectuer",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Texte à traiter (ou chemin du fichier d'entrée)",
    )

    # Arguments classiques
    parser.add_argument("--shift", type=int, help="Décalage pour César")
    parser.add_argument("--a", type=int, help="Coefficient a pour Affine")
    parser.add_argument("--b", type=int, help="Coefficient b pour Affine")
    parser.add_argument("--key", type=str, help="Clé pour Vigenère, DES, AES")

    # Arguments modernes
    parser.add_argument("--pub", help="Chemin du fichier de clé publique (pour RSA)")
    parser.add_argument("--priv", help="Chemin du fichier de clé privée (pour RSA)")
    parser.add_argument(
        "--out",
        help="Chemin du fichier de sortie (pour la génération RSA ou le résultat de chiffrement)",
    )

    args = parser.parse_args()

    content = _read_content(args.text)

    try:
        # --- Algorithmes classiques ---
        if args.method == "caesar":
            if args.shift is None:
                print("Erreur: --shift est requis pour César.", file=sys.stderr)
                sys.exit(1)
            if content is None:
                print("Erreur: Texte requis pour César.", file=sys.stderr)
                sys.exit(1)
            if args.action == "encrypt":
                print(crypto_utils.caesar_encrypt(content, args.shift))
            elif args.action == "decrypt":
                print(crypto_utils.caesar_decrypt(content, args.shift))

        elif args.method == "affine":
            if args.a is None or args.b is None:
                print("Erreur: --a et --b sont requis pour Affine.", file=sys.stderr)
                sys.exit(1)
            if content is None:
                print("Erreur: Texte requis pour Affine.", file=sys.stderr)
                sys.exit(1)
            if args.action == "encrypt":
                print(crypto_utils.affine_encrypt(content, args.a, args.b))
            elif args.action == "decrypt":
                print(crypto_utils.affine_decrypt(content, args.a, args.b))

        elif args.method == "vigenere":
            if not args.key:
                print("Erreur: --key est requise pour Vigenère.", file=sys.stderr)
                sys.exit(1)
            if content is None:
                print("Erreur: Texte requis pour Vigenère.", file=sys.stderr)
                sys.exit(1)
            if args.action == "encrypt":
                print(crypto_utils.vigenere_encrypt(content, args.key))
            elif args.action == "decrypt":
                print(crypto_utils.vigenere_decrypt(content, args.key))

        # --- Algorithmes modernes ---
        elif args.method == "aes":
            if not args.key:
                print("Erreur: --key est requise pour AES.", file=sys.stderr)
                sys.exit(1)
            if content is None:
                print("Erreur: Texte requis pour AES.", file=sys.stderr)
                sys.exit(1)
            key_bytes = _prepare_aes_key(args.key)

            if args.action == "encrypt":
                encrypted_bytes = crypto_utils.aes_encrypt(content, key_bytes)
                print(encrypted_bytes.hex())
            elif args.action == "decrypt":
                data_bytes = _hex_to_bytes(content, "AES")
                print(crypto_utils.aes_decrypt(data_bytes, key_bytes))

        elif args.method == "des":
            if not args.key:
                print("Erreur: --key est requise pour DES.", file=sys.stderr)
                sys.exit(1)
            if content is None:
                print("Erreur: Texte requis pour DES.", file=sys.stderr)
                sys.exit(1)
            key_bytes = _prepare_des_key(args.key)

            if args.action == "encrypt":
                encrypted_bytes = crypto_utils.des_encrypt(content, key_bytes)
                print(encrypted_bytes.hex())
            elif args.action == "decrypt":
                data_bytes = _hex_to_bytes(content, "DES")
                print(crypto_utils.des_decrypt(data_bytes, key_bytes))

        elif args.method == "rsa":
            if args.action == "generate-keys":
                priv, pub = crypto_utils.generate_rsa_keys()
                base = args.out if args.out else "id_rsa"
                with open(base, "wb") as f:
                    f.write(priv)
                with open(base + ".pub", "wb") as f:
                    f.write(pub)
                print(f"Clés générées: {base} et {base}.pub")

            elif args.action == "encrypt":
                if not args.pub:
                    print(
                        "Erreur: --pub <fichier_clé_publique> est requis pour le chiffrement RSA.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                if content is None:
                    print("Erreur: Texte requis pour le chiffrement RSA.", file=sys.stderr)
                    sys.exit(1)
                with open(args.pub, "rb") as f:
                    pub_key = f.read()
                encrypted_bytes = crypto_utils.rsa_encrypt(content, pub_key)
                print(encrypted_bytes.hex())

            elif args.action == "decrypt":
                if not args.priv:
                    print(
                        "Erreur: --priv <fichier_clé_privée> est requis pour le déchiffrement RSA.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                if content is None:
                    print("Erreur: Texte chiffré requis pour le déchiffrement RSA.", file=sys.stderr)
                    sys.exit(1)
                with open(args.priv, "rb") as f:
                    priv_key = f.read()
                data_bytes = _hex_to_bytes(content, "RSA")
                print(crypto_utils.rsa_decrypt(data_bytes, priv_key))

    except (ValueError, TypeError) as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Erreur: Fichier non trouvé — {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
