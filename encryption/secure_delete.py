import os


def secure_delete(file_path):

    if os.path.exists(file_path):

        with open(file_path, "ba+", buffering=0) as file:

            length = file.tell()

            file.seek(0)

            file.write(os.urandom(length))

        os.remove(file_path)