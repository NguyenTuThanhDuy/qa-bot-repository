from fastapi import APIRouter, Depends, HTTPException, Request
import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session

from ai.embedding_vector import EmbeddingVector
from database.db_connector import get_db_session
from qa_app.validation_models.qa_validation_model import QARequest, VectorResponseModel
from qa_app.models.question_model import QAHistory

router = APIRouter()


@router.post("/", response_model=VectorResponseModel, description="Convert text to vector")
def api_get_vector_by_text(request: Request, question_request: QARequest, db: Session = Depends(get_db_session)):
    embed = EmbeddingVector()
    res = embed.create_embedding_vector(question_request.input_text)
    record = QAHistory(
        input_text=question_request.input_text,
        embedded_vector=res
    )
    db.add(record)
    db.commit()
    return VectorResponseModel(input_text=question_request.input_text, vector=res)

@router.post("/search", description="Search similarity sentences")
def api_get_vector_by_text(request: Request, question_request: QARequest, db: Session = Depends(get_db_session)):
    embed = EmbeddingVector()
    query_vector = embed.create_embedding_vector(question_request.input_text)
    raw_sql = """
        SELECT input_text
        FROM qa_history
        ORDER BY embedded_vector <=> :query_vector
        LIMIT :k
    """
    
    # Execute the query with parameters
    result = db.execute(text(raw_sql), {"query_vector": query_vector, "k": 3})
    return result.fetchall()
