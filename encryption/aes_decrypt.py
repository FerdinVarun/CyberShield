from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_file(input_file_path, output_file_path, secret_key):

    with open(input_file_path, 'rb') as file:

        file_data = file.read()

    # Extract IV
    iv = file_data[:16]

    encrypted_data = file_data[16:]

    # Create cipher
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    # Decrypt data
    decrypted_data = unpad(
        cipher.decrypt(encrypted_data),
        AES.block_size
    )

    # Save decrypted file
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)