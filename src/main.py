import os
import time
import logging
from typing import List
from http import HTTPStatus

import structlog
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder

from dto.base_dto import ErrorReponse
from config import BaseConfig as Conf
from routes import api_router
from middleware.before_intercepter import BeforeInterceptor


def create_app(app_name: str = Conf.PROJECT_NAME) -> FastAPI:
    """Create a FastApi app."""

    app: FastAPI = FastAPI(title=app_name)

    app.add_middleware(BeforeInterceptor)

    app.include_router(api_router, prefix=Conf.API_V1_STR)

    @app.exception_handler(Exception)
    def general_exception_handler(request: Request, exc: Exception) -> ErrorReponse:

        if isinstance(exc, RequestValidationError):
            errors = exc.errors()
            filtered_errors: List[dict] = [
                dict(
                    msg=error.get("msg"),
                    type=error.get("type"),
                    loc=error.get("loc"),
                )
                for error in errors
            ]

            return JSONResponse(
                content=ErrorReponse(
                    message=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                    data=jsonable_encoder(filtered_errors)
                ),
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value
            )

        # NOTE: any other exception will be treated as internal server error

        return PlainTextResponse(
            content=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
        )

    return app


def config_timezone(tz: str = Conf.TIMEZONE):
    """
        Configure timezone for the entire process, default is Asia/Tokyo.
    """

    os.environ['TZ'] = tz
    time.tzset()


def config_logging():
    """
        Configure to use "structlog" so that you can output log according to structure.
    """

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(level=logging.DEBUG)


config_timezone()
config_logging()
app: FastAPI = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host=Conf.HOST,
        port=Conf.PORT,
        reload=Conf.RELOAD,
        workers=Conf.WORKERS
    )
# NOTE: This workers configuration only run when reload is False
