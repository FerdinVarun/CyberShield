from database.db import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()


# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL
)
""")


# ENCRYPTED FILES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS encrypted_files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    original_filename TEXT NOT NULL,

    encrypted_filename TEXT NOT NULL,

    password_hash TEXT NOT NULL,

    encrypted_secret_key BLOB NOT NULL,

    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    expiry_time TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
)
""")

conn.commit()

print("Database initialized successfully.")