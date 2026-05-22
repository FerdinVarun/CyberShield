from encryption.password_handler import hash_password, verify_password

password = "mypassword123"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

result = verify_password(password, hashed)

print("Password Match:", result)