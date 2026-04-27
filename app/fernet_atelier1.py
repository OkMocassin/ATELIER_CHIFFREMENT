import os
import sys
from cryptography.fernet import Fernet


def get_key():
    key = os.environ.get("FERNET_KEY")
    if not key:
        print("❌ FERNET_KEY non défini (GitHub Secret ou export local)")
        sys.exit(1)
    return key.encode()


def encrypt(input_file, output_file):
    key = get_key()
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted)

    print("✅ Fichier chiffré")


def decrypt(input_file, output_file):
    key = get_key()
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    try:
        decrypted = f.decrypt(data)
    except Exception:
        print("❌ Échec du déchiffrement (clé incorrecte ou fichier altéré)")
        sys.exit(1)

    with open(output_file, "wb") as file:
        file.write(decrypted)

    print("✅ Fichier déchiffré")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fernet_atelier1.py [encrypt|decrypt] input output")
        sys.exit(1)

    action, input_file, output_file = sys.argv[1:]

    if action == "encrypt":
        encrypt(input_file, output_file)
    elif action == "decrypt":
        decrypt(input_file, output_file)
    else:
        print("❌ Action inconnue : encrypt ou decrypt uniquement")