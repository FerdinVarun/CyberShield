from cryptography.fernet import Fernet

master_key = Fernet.generate_key()

with open("master.key", "wb") as key_file:
    key_file.write(master_key)

print("Master key generated successfully.")