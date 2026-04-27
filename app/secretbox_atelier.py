import os
import sys
from nacl.secret import SecretBox
from nacl.utils import Random


def get_key():
    key = os.environ.get("SECRETBOX_KEY")
    if not key:
        print("❌ SECRETBOX_KEY non défini")
        sys.exit(1)
    return bytes.fromhex(key)


def encrypt(input_file, output_file):
    key = get_key()
    box = SecretBox(key)

    with open(input_file, "rb") as f:
        data = f.read()

    nonce = Random(SecretBox.NONCE_SIZE)
    encrypted = box.encrypt(data, nonce)

    with open(output_file, "wb") as f:
        f.write(encrypted)

    print("✅ Fichier chiffré avec SecretBox")


def decrypt(input_file, output_file):
    key = get_key()
    box = SecretBox(key)

    with open(input_file, "rb") as f:
        data = f.read()

    try:
        decrypted = box.decrypt(data)
    except Exception:
        print("❌ Déchiffrement impossible (clé ou fichier modifié)")
        sys.exit(1)

    with open(output_file, "wb") as f:
        f.write(decrypted)

    print("✅ Fichier déchiffré avec SecretBox")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python secretbox_atelier.py [encrypt|decrypt] input output")
        sys.exit(1)

    action, input_file, output_file = sys.argv[1:]

    if action == "encrypt":
        encrypt(input_file, output_file)
    elif action == "decrypt":
        decrypt(input_file, output_file)
    else:
        print("❌ Action invalide")