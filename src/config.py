import os
import logging
from http import HTTPStatus
from typing import List, Literal

from dotenv import load_dotenv

load_dotenv()


class APIConfig(object):
    API_V1_STR: str = '/api/v1'
    DEFAULT_API_RESPONSES: dict = {
        HTTPStatus.NOT_FOUND.value: {
            "description": HTTPStatus.NOT_FOUND.phrase
        }
    }


class CORSConfig(object):
    # origins
    FRONTEND_DOMAIN: str = os.getenv("FRONTEND_DOMAIN", "")
    FRONTEND_URL: str = f"https://{FRONTEND_DOMAIN}"
    BASE_ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000"
    ]
    ALLOWED_ORIGINS: List[str] = BASE_ALLOWED_ORIGINS + [FRONTEND_URL] if FRONTEND_URL else BASE_ALLOWED_ORIGINS

    # headers
    ALLOWED_HEADERS: List[str] = [
        "Host",
        "Connection",
        "User-Agent",
        "Accept",
        "Authorization",
        "Origin",
        "Referer",
        "Accept-Encoding",
        "Accept-Language"
    ]

    # methods
    ALLOWED_METHODS: List[str] = []


class ServerConfig(object):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    RELOAD: bool = bool(os.getenv("RELOAD")) or False
    # NOTE: This workers configuration only run when reload is False
    WORKERS: int = int(os.getenv("WORKERS", 1))

    # server environment
    ENVIRONMENT_POC = 'poc'
    ENVIRONMENT_DEV = 'dev'
    ENVIRONMENT_PROD = 'prod'
    ENVIRONMENT = os.getenv('ENVIRONMENT', ENVIRONMENT_PROD)

    MOCK_SECRET = os.getenv('MOCK_SECRET')


class BaseConfig(
    APIConfig,
    CORSConfig,
    ServerConfig
):
    PROJECT_NAME: str = "Knowledge Base"
    TIMEZONE: str = "Asia/Ho_Chi_Minh"
    LOGGING_LEVEL: Literal[
        'CRITICAL',
        'FATAL',
        'ERROR',
        'WARN',
        'WARNING',
        'INFO',
        'DEBUG',
        'NOTSET'
    ] = logging._nameToLevel.get(os.getenv("LOGGING_LEVEL", "INFO"))
