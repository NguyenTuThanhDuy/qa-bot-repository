from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.schema import Index

from pgvector.sqlalchemy import Vector  # Use if you're leveraging pgvector for vector search
from database.postgres_db.base_model import Base


class QAHistory(Base):
    __tablename__ = "qa_history"

    qa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Serial-like behavior
    input_text = Column(Text, nullable=False)  # Unlimited character length
    embedded_vector = Column(Vector(1536), nullable=True)  # Stores a list of floats
    created_at = Column(DateTime, server_default=func.now())  # Auto timestamp

    __table_args__ = (
        Index('qa_history_vector_idx', embedded_vector, postgresql_using='ivfflat'),
    )

    @classmethod
    def prepare_sql_stmt(cls):
        """
        <=> - Cosine Distance = 1 - Cosine Similarity (Low distance means they are similar)
        """
        return """
            SELECT qa_id, input_text, 1 - (embedded_vector <=> CAST(:query_vector AS Vector)) AS similarity
            FROM qa_history
            WHERE embedded_vector <=> CAST(:query_vector AS Vector) < 0.3
            ORDER BY similarity
            LIMIT 5
        """
