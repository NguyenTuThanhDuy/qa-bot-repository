from typing import List

from pydantic import BaseModel


class QARequest(BaseModel):
    input_text: str

class VectorResponseModel(QARequest):
    vector: List[float]
