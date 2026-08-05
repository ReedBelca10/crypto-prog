# Crypto Prog

![Python Version](https://img.shields.io/badge/Tested%20on-Python%203.10%2B-blue)
[![Français](https://img.shields.io/badge/Langue-Fran%C3%A7ais-red)](README.md)

This project provides a simple Command Line Interface (CLI) and a modern Graphical User Interface (GUI) along with a Python library (`crypto_utils`) for various encryption algorithms, ranging from classic (Caesar, Affine, Vigenère) to modern (RSA, DES, AES).

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Graphical User Interface (GUI)

For a more user-friendly experience, launch the GUI:

```bash
python crypto_gui.py
```

The modernized interface (built with CustomTkinter) allows you to select algorithms, input text or load files, and easily manage your RSA keys. It also features a built-in User Guide accessible via the sidebar menu.

### Command Line Interface (CLI)

You can also use the `crypto_cli.py` script to access all features directly from the terminal.

### Classic Algorithms

> [!WARNING]
> Classic algorithms (Caesar, Affine, Vigenère) are provided for educational purposes only. They do not offer modern cryptographic security.

**Caesar Cipher:**
```bash
python crypto_cli.py caesar encrypt "HELLO WORLD" --shift 3
python crypto_cli.py caesar decrypt "KHOOR ZRUOG" --shift 3
```

**Affine Cipher:**
```bash
python crypto_cli.py affine encrypt "HELLO" --a 5 --b 8
python crypto_cli.py affine decrypt "RCLLA" --a 5 --b 8
```

**Vigenère Cipher:**
```bash
python crypto_cli.py vigenere encrypt "HELLO" --key "KEY"
python crypto_cli.py vigenere decrypt "RIJVS" --key "KEY"
```

### Modern Algorithms

**AES (Advanced Encryption Standard):**
```bash
# Encrypt (Output is in hexadecimal)
python crypto_cli.py aes encrypt "Secret Message" --key "mysecretkey12345"

# Decrypt (Input must be hexadecimal)
python crypto_cli.py aes decrypt "<hex_output>" --key "mysecretkey12345"
```

**RSA (Rivest–Shamir–Adleman):**
```bash
# Generate keys
python crypto_cli.py rsa generate-keys --out my_key

# Encrypt
python crypto_cli.py rsa encrypt "Secret Message" --pub my_key.pub

# Decrypt
python crypto_cli.py rsa decrypt "<hex_output>" --priv my_key
```

For more details, check out the built-in guide in the GUI or read [USER_GUIDE.md](USER_GUIDE.md).

## Library Usage

You can also use the `crypto_utils` module in your own Python scripts. It now features full type hinting and robust error handling!

```python
import crypto_utils
try:
    ciphertext = crypto_utils.caesar_encrypt("HELLO", 3)
    print(ciphertext)
except ValueError as e:
    print(e)
```

## Tests

This project includes a comprehensive test suite using `pytest`.
```bash
pytest tests/
```
