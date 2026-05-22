

def allowed_file(filename):
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from config import ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from utils.logger import log_activity
from datetime import datetime, timedelta
import os
import uuid
from utils.validators import (
    validate_file_size,
    allowed_file
)
from encryption.aes_encrypt import encrypt_file
from encryption.password_handler import hash_password
from encryption.key_manager import encrypt_secret_key

from database.db import get_db_connection

from config import ENCRYPTED_FOLDER
from config import UPLOAD_FOLDER

encrypt_bp = Blueprint(
    'encrypt_bp',
    __name__
)


@encrypt_bp.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():

    # LOGIN PROTECTION
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        uploaded_file = request.files['file']

        password = request.form['password']

        if secure_filename(uploaded_file.filename) == '':
            return "No file selected"
        if not allowed_file(secure_filename(uploaded_file.filename)):
            return "File type not allowed"
        # Save uploaded file
        original_path = os.path.join(
            UPLOAD_FOLDER,
            secure_filename(uploaded_file.filename)
        )

        uploaded_file.save(original_path)

        # Random encrypted filename
        encrypted_filename = (
            str(uuid.uuid4()) + ".bin"
        )

        encrypted_path = os.path.join(
            ENCRYPTED_FOLDER,
            encrypted_filename
        )

        # Encrypt file
        secret_key = encrypt_file(
            original_path,
            encrypted_path
        )

        # Hash password
        hashed_password = hash_password(password)

        # Encrypt AES key
        encrypted_secret_key = encrypt_secret_key(
            secret_key
        )
        expiry_time = (
            datetime.now() + timedelta(hours=24)
        )
        # Store in DB
        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO encrypted_files (

            user_id,

            original_filename,

            encrypted_filename,

            password_hash,

            encrypted_secret_key,

            expiry_time

        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            session['user_id'],

            secure_filename(uploaded_file.filename),

            encrypted_filename,

            hashed_password,

            encrypted_secret_key,

            expiry_time
            ))

        conn.commit()

        conn.close()
        log_activity(
            f"{session['username']} encrypted file: {secure_filename(uploaded_file.filename)}"
        )
        return f"""
        File encrypted successfully.<br><br>

        Encrypted Filename:<br>
        {encrypted_filename}
        """

    return render_template('encrypt.html')