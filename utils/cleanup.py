from datetime import datetime

from database.db import get_db_connection

from encryption.secure_delete import secure_delete

from config import ENCRYPTED_FOLDER

import os


def cleanup_expired_files():

    conn = get_db_connection()

    cursor = conn.cursor()

    current_time = datetime.now()

    cursor.execute("""
    SELECT *
    FROM encrypted_files
    WHERE expiry_time <= ?
    """, (current_time,))

    expired_files = cursor.fetchall()

    for file in expired_files:

        encrypted_path = os.path.join(
            ENCRYPTED_FOLDER,
            file['encrypted_filename']
        )

        secure_delete(encrypted_path)

        cursor.execute("""
        DELETE FROM encrypted_files
        WHERE id = ?
        """, (file['id'],))

    conn.commit()

    conn.close()

    print("Expired files cleaned.")