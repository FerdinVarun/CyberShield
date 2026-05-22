
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os

from flask import Flask, request, redirect, render_template

from config import *

from routes.encrypt_routes import encrypt_bp
from routes.decrypt_routes import decrypt_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

csrf = CSRFProtect(app)
Talisman(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.before_request
def force_https():
    if not request.is_secure and os.environ.get("RENDER"):
        return redirect(request.url.replace("http://", "https://"))


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ENCRYPTED_FOLDER"] = ENCRYPTED_FOLDER
app.config["DECRYPTED_FOLDER"] = DECRYPTED_FOLDER
app.config["SECRET_KEY"] = SECRET_KEY


# Register Blueprints
app.register_blueprint(encrypt_bp)
app.register_blueprint(decrypt_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()