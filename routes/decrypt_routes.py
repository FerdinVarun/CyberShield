from flask import Blueprint, render_template, request, send_file
import os
from flask import session
from flask import redirect
from utils.logger import log_activity
from encryption.aes_decrypt import decrypt_file
from encryption.password_handler import verify_password
from encryption.key_manager import decrypt_secret_key

from database.db import get_db_connection

from config import ENCRYPTED_FOLDER, DECRYPTED_FOLDER

decrypt_bp = Blueprint('decrypt_bp', __name__)


@decrypt_bp.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():

    # LOGIN REQUIRED
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        encrypted_filename = request.form['filename']

        password = request.form['password']

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM encrypted_files
        WHERE encrypted_filename = ?
         AND user_id = ?
        """, (encrypted_filename, session['user_id']))

        file_record = cursor.fetchone()

        if file_record is None:
            conn.close()
            return "File not found"

        stored_password_hash = file_record['password_hash']

        # Verify password
        password_correct = verify_password(
            password,
            stored_password_hash
        )

        if not password_correct:
            conn.close()
            return "Wrong password"

        # Decrypt AES key
        encrypted_secret_key = file_record['encrypted_secret_key']

        secret_key = decrypt_secret_key(
            encrypted_secret_key
        )

        encrypted_file_path = os.path.join(
            ENCRYPTED_FOLDER,
            encrypted_filename
        )

        decrypted_filename = (
            "decrypted_" +
            file_record['original_filename']
        )

        decrypted_file_path = os.path.join(
            DECRYPTED_FOLDER,
            decrypted_filename
        )

        # Decrypt file
        decrypt_file(
            encrypted_file_path,
            decrypted_file_path,
            secret_key
        )

        # DELETE database record after decrypt
        cursor.execute("""
        DELETE FROM encrypted_files
        WHERE id = ?
        """, (file_record['id'],))

        conn.commit()

        conn.close()
        log_activity(
            f"{session['username']} decrypted file: {decrypted_filename}"
        )

        return send_file(
            decrypted_file_path,
            as_attachment=True
        )

    return render_template('decrypt.html')