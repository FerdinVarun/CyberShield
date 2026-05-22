import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret_key")
DATABASE_URL = os.environ.get("DATABASE_URL")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ENCRYPTED_FOLDER = os.path.join(BASE_DIR, "encrypted_files")
DECRYPTED_FOLDER = os.path.join(BASE_DIR, "decrypted_files")
TEMP_FOLDER = os.path.join(BASE_DIR, "temp")

MAX_CONTENT_LENGTH = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg',
    'docx', 'xlsx', 'pptx'
}
