from typing import List
import logging

from pydantic import TypeAdapter
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from ai.embedding_vector import EmbeddingVector
from database.db_connector import get_db_session
from qa_app.validation_models.qa_validation_model import QARequest, QAResponseModel, QASearchResponseModel
from database.models import QAHistory


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=QAResponseModel, description="Convert text to vector")
def api_get_vector_by_text(request: Request, question_request: QARequest, db: Session = Depends(get_db_session)):
    try:
        embed = EmbeddingVector()
        res = embed.create_embedding_vector(input_text=question_request.input_text)
        record = QAHistory(
            input_text=question_request.input_text,
            embedded_vector=res
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return QAResponseModel(input_text=question_request.input_text, qa_id=record.qa_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=403, detail="Error when insert QAHistory record")


@router.post("/search", response_model=List[QASearchResponseModel], description="Search similarity sentences")
def api_get_vector_by_text(request: Request, question_request: QARequest, db: Session = Depends(get_db_session)):
    try:
        embed = EmbeddingVector()
        query_vector = embed.create_embedding_vector(input_text=question_request.input_text)

        result = db.execute(text(QAHistory.prepare_sql_stmt()), {"query_vector": query_vector})

        return TypeAdapter(List[QASearchResponseModel]).validate_python(result.mappings().all())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=403, detail="Error when searching QAHistory record")
