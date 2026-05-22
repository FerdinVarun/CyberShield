from encryption.aes_encrypt import encrypt_file
from encryption.aes_decrypt import decrypt_file

input_file = "sample.txt"

encrypted_file = "encrypted_files/sample_encrypted.bin"

decrypted_file = "decrypted_files/sample_decrypted.txt"


# Encrypt
secret_key = encrypt_file(input_file, encrypted_file)

print("File encrypted successfully.")


# Decrypt
decrypt_file(encrypted_file, decrypted_file, secret_key)

print("File decrypted successfully.")