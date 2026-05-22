ALLOWED_EXTENSIONS = {
    'txt',
    'pdf',
    'png',
    'jpg',
    'jpeg',
    'docx'
}


def allowed_file(filename):

    return (
        '.' in filename
        and
        filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def validate_file_size(file):

    MAX_SIZE = 50 * 1024 * 1024

    file.seek(0, 2)

    size = file.tell()

    file.seek(0)

    if size > MAX_SIZE:
        return False

    return True