from sqlalchemy import Column, Integer, Text, DateTime, func

from pgvector.sqlalchemy import Vector  # Use if you're leveraging pgvector for vector search
from database.postgres_db.base_model import Base


class QAHistory(Base):
    __tablename__ = "qa_history"

    qa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Serial-like behavior
    input_text = Column(Text, nullable=False)  # Unlimited character length
    embedded_vector = Column(Vector(1536), nullable=True)  # Stores a list of floats
    created_at = Column(DateTime, server_default=func.now())  # Auto timestamp
