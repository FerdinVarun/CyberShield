from datetime import datetime


def log_activity(message):

    with open(
        "logs/activity.log",
        "a"
    ) as log_file:

        log_file.write(
            f"[{datetime.now()}] {message}\n"
        )