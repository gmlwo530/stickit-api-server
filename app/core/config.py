from dotenv import load_dotenv

import os

load_dotenv()

API_V1_STR = "/api/v1"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

ROLE_SUPERUSER = "superuser"

SERVER_NAME = os.environ["SERVER_NAME"]
SECRET_KEY = os.environ["SECRET_KEY"]

UPLOAD_DIR_NAME = os.environ["UPLOAD_DIR_NAME"]
