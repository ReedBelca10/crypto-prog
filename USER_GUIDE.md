# Guide Utilisateur

Ce guide explique les algorithmes pris en charge par l'outil Crypto Prog et comment les utiliser via l'interface graphique ou la ligne de commande.

## Interface Graphique (GUI)

L'interface graphique modernisée (`crypto_gui.py`) offre une manière intuitive d'utiliser l'outil, divisée en deux onglets principaux (Outil de Chiffrement et Guide Utilisateur) :

1.  **Algorithme** : Sélectionnez la méthode de chiffrement en haut.
2.  **Paramètres** : Les champs s'adaptent automatiquement (Décalage, Clé, etc.).
3.  **Entrée** : Saisissez votre texte directement ou utilisez le bouton "Charger Fichier" pour lire un fichier texte.
4.  **Actions** : Cliquez sur "CHIFFRER" ou "DÉCHIFFRER".
5.  **Sortie** : Le résultat s'affiche en bas. Vous pouvez le sauvegarder dans un fichier avec le bouton "Sauvegarder Résultat".
6.  **RSA Special** : Pour RSA, l'interface inclut un bouton "Générer Clés" pour créer facilement vos paires de clés.
7.  **Guide Intégré** : Vous pouvez à tout moment consulter ce guide utilisateur directement depuis le menu latéral de l'application !

## Algorithmes Classiques

Ces algorithmes sont historiquement significatifs mais **non sécurisés** selon les normes modernes. Utilisez-les uniquement à des fins éducatives.

### 1. Chiffre de César
Un chiffrement par substitution simple où chaque lettre est décalée d'un nombre fixe de positions.
- **Paramètres :** `shift` (entier)

### 2. Chiffre Affine
Un chiffrement par substitution utilisant la fonction `E(x) = (ax + b) mod 26`.
- **Paramètres :** `a` (doit être premier avec 26), `b` (tout entier)

### 3. Chiffre de Vigenère
Un chiffrement par substitution polyalphabétique utilisant un mot-clé.
- **Paramètres :** `key` (chaîne de caractères)

## Algorithmes Modernes

Ces implémentations utilisent la bibliothèque `cryptography` et sont plus robustes.

### 1. AES (Advanced Encryption Standard)
L'un des algorithmes de chiffrement symétrique les plus sécurisés.
- **Mode :** CBC (Cipher Block Chaining)
- **Clé :** Hachage automatique vers 128/192/256 bits si la longueur exacte n'est pas fournie.
- **Sortie :** Chaîne encodée en hexadécimal (IV + Texte chiffré).

### 2. DES (Data Encryption Standard)
Un algorithme symétrique plus ancien. Nous utilisons TripleDES (3DES) pour une meilleure compatibilité et une légère amélioration de la sécurité par rapport au DES brut, bien qu'il soit toujours considéré comme obsolète.
- **Mode :** CBC
- **Clé :** Ajustée automatiquement à une longueur valide.

### 3. RSA (Rivest–Shamir–Adleman)
Chiffrement asymétrique utilisant une paire de clés publique et privée.
- **Flux de travail :**
    1. Générer une paire de clés (`generate-keys`).
    2. Partager la **Clé Publique** (`.pub`).
    3. L'expéditeur chiffre avec la Clé Publique.
    4. Le destinataire déchiffre avec la **Clé Privée**.
- **Remplissage (Padding) :** OAEP avec SHA256.

## Dépannage

- **"Le texte d'entrée doit être une chaîne hexadécimale"** : Lors du déchiffrement des algorithmes modernes, l'entrée doit être la chaîne hexadécimale obtenue lors de l'étape de chiffrement.
- **"Le coefficient 'a' n'a pas d'inverse"** : Pour le chiffre Affine, `a` doit être premier avec 26 (par exemple, 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25).
