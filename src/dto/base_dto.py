from typing import Any
from pydantic import BaseModel


class ErrorReponse(BaseModel):
    message: str
    data: Any
