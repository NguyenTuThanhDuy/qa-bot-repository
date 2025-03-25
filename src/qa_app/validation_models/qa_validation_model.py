from pydantic import BaseModel

class QARequest(BaseModel):
    input_text: str

class QAResponseModel(QARequest):
    qa_id: int

class QASearchResponseModel(QAResponseModel):
    similarity: float
