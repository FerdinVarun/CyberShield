from encryption.key_manager import encrypt_secret_key, decrypt_secret_key

secret_key = b"my_super_secret_key"

encrypted = encrypt_secret_key(secret_key)

print("Encrypted Key:")
print(encrypted)

decrypted = decrypt_secret_key(encrypted)

print("Decrypted Key:")
print(decrypted)