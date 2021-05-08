import random
import string

from app.core import config


def get_server_api():
    return f"http://{config.SERVER_NAME}"


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
