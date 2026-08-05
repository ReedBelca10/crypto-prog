# Programme de Cryptographie

![Python Version](https://img.shields.io/badge/Test%C3%A9%20sur-Python%203.10%2B-blue)
[![English](https://img.shields.io/badge/Language-English-red)](README_EN.md)

Ce projet fournit une interface en ligne de commande (CLI) simple et une bibliothèque Python (`crypto_utils`) pour divers algorithmes de chiffrement, allant des classiques (César, Affine, Vigenère) aux modernes (RSA, DES, AES).

## Installation

1. Clonez ou téléchargez ce dépôt.
2. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

## Utilisation
### Interface Graphique (GUI)

Pour une utilisation plus conviviale, lancez l'interface graphique :

```bash
python crypto_gui.py
```

L'interface modernisée vous permet de choisir l'algorithme, de saisir du texte ou de charger un fichier, et de gérer vos clés RSA facilement. Elle intègre également le guide utilisateur directement consultable depuis l'application via l'onglet "Guide Utilisateur".

### Ligne de Commande (CLI)

Vous pouvez également utiliser le script `crypto_cli.py` pour accéder à toutes les fonctionnalités via le terminal.

### Algorithmes Classiques

**Chiffrement de César:**
```bash
python crypto_cli.py caesar encrypt "BONJOUR MONDE" --shift 3
python crypto_cli.py caesar decrypt "ERQmRXU PRQGH" --shift 3
```

**Chiffrement Affine:**
```bash
python crypto_cli.py affine encrypt "BONJOUR" --a 5 --b 8
python crypto_cli.py affine decrypt "RESULTAT" --a 5 --b 8
```

**Chiffrement de Vigenère:**
```bash
python crypto_cli.py vigenere encrypt "BONJOUR" --key "CLE"
python crypto_cli.py vigenere decrypt "DZYHVZE" --key "CLE"
```

### Algorithmes Modernes

**AES:**
```bash
# Chiffrer (La sortie est en hexadécimal)
python crypto_cli.py aes encrypt "Message Secret" --key "maclefscrete12345"

# Déchiffrer (L'entrée doit être en hexadécimal)
python crypto_cli.py aes decrypt "<sortie_hex>" --key "maclefscrete12345"
```

**RSA:**
```bash
# Générer les clés
python crypto_cli.py rsa generate-keys --out ma_cle

# Chiffrer
python crypto_cli.py rsa encrypt "Message Secret" --pub ma_cle.pub

# Déchiffrer
python crypto_cli.py rsa decrypt "<sortie_hex>" --priv ma_cle
```

Pour plus de détails, consultez le [GUIDE_UTILISATEUR.md](USER_GUIDE.md).

## Utilisation de la Bibliothèque

Vous pouvez également utiliser le module `crypto_utils` dans vos propres scripts Python :

```python
import crypto_utils
chiffre = crypto_utils.caesar_encrypt("BONJOUR", 3)
```
