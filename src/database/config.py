import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_CONNECTION_ENGINE = "postgresql://"
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")
    POSTGRES_CONNECTION_URL = f"{POSTGRES_CONNECTION_ENGINE}{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
