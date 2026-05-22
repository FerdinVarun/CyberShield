from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import os


def encrypt_file(input_file_path, output_file_path):

    # Generate AES-256 key
    secret_key = get_random_bytes(32)

    # Generate IV
    iv = get_random_bytes(16)

    # Create AES cipher
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    # Read original file
    with open(input_file_path, 'rb') as file:
        file_data = file.read()

    # Encrypt data
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

    # Save encrypted file
    with open(output_file_path, 'wb') as file:
        file.write(iv + encrypted_data)

    return secret_key