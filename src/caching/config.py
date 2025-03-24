import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "1"))
    REDIS_SOCKET_TIMEOUT = 5
