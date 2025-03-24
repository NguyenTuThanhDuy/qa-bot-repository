import functools
from http import HTTPMethod, HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import ALL_METHODS, SAFELISTED_HEADERS

from config import BaseConfig as Conf

ALLOW_ALL = "*"


def allow_cors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)

        # CORS config
        allow_origins: list = Conf.ALLOWED_ORIGINS or [ALLOW_ALL]
        allow_credentials: bool = True
        allow_methods: list = Conf.ALLOWED_METHODS or ALL_METHODS
        allow_headers: list = Conf.ALLOWED_HEADERS or SAFELISTED_HEADERS
        max_age: int = 600

        # prepare allow configs

        # methods
        if ALLOW_ALL in allow_methods:
            allow_methods = ALL_METHODS

        # origins
        if ALLOW_ALL in allow_origins:
            allow_origins = [ALLOW_ALL]
        else:
            request: Request = args[1]
            client_origin: str = request.headers.get("origin")
            allow_origins = [client_origin] if client_origin in allow_origins else []

        # headers
        if ALLOW_ALL in allow_headers:
            allow_headers = [ALLOW_ALL]
        else:
            allow_headers = sorted(SAFELISTED_HEADERS | set(allow_headers))

        response.headers["Access-Control-Allow-Credentials"] = "true" if allow_credentials else "false"
        response.headers['Access-Control-Allow-Origin'] = ", ".join(allow_origins)
        response.headers['Access-Control-Allow-Methods'] = ", ".join(allow_methods)
        response.headers['Access-Control-Allow-Headers'] = ", ".join(allow_headers)
        response.headers["Access-Control-Max-Age"] = str(max_age)

        return response
    return wrapper


class BeforeInterceptor(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    @allow_cors
    async def dispatch(self, request: Request, call_next):
        if request.method == HTTPMethod.OPTIONS:
            return PlainTextResponse(
                content=HTTPStatus.OK.phrase,
                status_code=HTTPStatus.OK.value
            )

        return await call_next(request)
