from cryptography.fernet import Fernet


with open("master.key", "rb") as key_file:
    master_key = key_file.read()

fernet = Fernet(master_key)


def encrypt_secret_key(secret_key):

    return fernet.encrypt(secret_key)


def decrypt_secret_key(encrypted_secret_key):

    return fernet.decrypt(encrypted_secret_key)