from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from database.db import get_db_connection

from encryption.password_handler import (
    hash_password,
    verify_password
)

auth_bp = Blueprint(
    'auth_bp',
    __name__
)
login_attempts = {}

# REGISTER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        hashed_password = hash_password(password)

        conn = get_db_connection()

        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO users (
                username,
                password_hash
            )
            VALUES (?, ?)
            """, (
                username,
                hashed_password
            ))

            conn.commit()

            conn.close()

            return redirect('/login')

        except:

            conn.close()

            return "Username already exists"

    return render_template('register.html')


# LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr

    if ip not in login_attempts:
        login_attempts[ip] = 0

    if login_attempts[ip] >= 5:
        return "Too many failed attempts"
    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return "User not found"

        password_correct = verify_password(
            password,
            user['password_hash']
        )

        if not password_correct:
            login_attempts[ip] += 1
            return "Wrong password"
        login_attempts[ip] = 0
        session['user_id'] = user['id']

        session['username'] = user['username']

        return redirect('/dashboard')

    return render_template('login.html')


# LOGOUT
@auth_bp.route('/logout')
def logout():

    session.clear()

    return redirect('/login')
