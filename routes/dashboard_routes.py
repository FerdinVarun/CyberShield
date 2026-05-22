from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from database.db import get_db_connection

dashboard_bp = Blueprint(
    'dashboard_bp',
    __name__
)


@dashboard_bp.route('/dashboard')
def dashboard():

    # LOGIN REQUIRED
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    cursor = conn.cursor()

    # ONLY SHOW USER FILES
    cursor.execute("""
    SELECT *
    FROM encrypted_files
    WHERE user_id = ?
    ORDER BY upload_time DESC
    """, (session['user_id'],))

    files = cursor.fetchall()

    conn.close()

    return render_template(
    'dashboard.html',
    files=files,
    username=session['username'],
    total_files=len(files)
    )