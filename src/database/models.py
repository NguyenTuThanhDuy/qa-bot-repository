from typing import List

from sqlalchemy import Integer, Text, DateTime, func, Table, ForeignKey, Column
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.schema import Index
from pgvector.sqlalchemy import Vector  # Use if you're leveraging pgvector for vector search


N_DIM = 512


class Base(DeclarativeBase):
    pass


class QAHistory(Base):
    __tablename__ = "qa_history"

    qa_id: Mapped[int] = mapped_column(Integer, name="qa_id", primary_key=True, autoincrement=True)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedded_vector: Mapped[List[float]] = mapped_column(Vector(N_DIM), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        # Index('qa_history_vector_idx', embedded_vector, postgresql_using='ivfflat'),
        Index(
            "qa_history_vector_idx",
            embedded_vector,
            postgresql_using="hnsw",
            postgresql_with={"m": 32, "ef_construction": 100},
            postgresql_ops={"embedded_vector": "vector_cosine_ops"}
        ),
    )

    @classmethod
    def prepare_sql_stmt(cls):
        """
        <=> - Cosine Distance = 1 - Cosine Similarity (Low distance means they are similar)
        """
        return """
            SELECT qa_id, input_text, 1 - (embedded_vector <=> CAST(:query_vector AS Vector)) AS similarity
            FROM qa_history
            WHERE embedded_vector <=> CAST(:query_vector AS Vector) < 0.4
            ORDER BY similarity
            LIMIT 5
        """


product_supplier_association = Table(
    "product_supplier",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True),
    Column("supplier_id", Integer, ForeignKey("supplier.supplier_id", ondelete="CASCADE"), primary_key=True),
)


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(Integer, name="product_id", primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(Text, name="product_name", unique=True)
    product_description: Mapped[str] = mapped_column(Text, name="product_description")
    product_description_vector: Mapped[List[float]] = mapped_column(Vector(N_DIM))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    suppliers: Mapped[List["Supplier"]] = relationship(
        "Supplier",
        secondary=product_supplier_association,
        back_populates="products",
        cascade="all, delete"
    )

    __table_args__ = (
        Index(
            "product_prd_description_vector_idx",
            product_description_vector,
            postgresql_using="hnsw",
            postgresql_with={"m": 32, "ef_construction": 100},
            postgresql_ops={"product_description_vector": "vector_cosine_ops"}
        ),
    )

class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id: Mapped[int] = mapped_column(Integer, name="supplier_id", primary_key=True, autoincrement=True)
    supplier_name: Mapped[str] = mapped_column(Text, name="supplier_name", unique=True)
    supplier_description: Mapped[str] = mapped_column(Text, name="product_description")
    supplier_description_vector: Mapped[List[float]] = mapped_column(Vector(N_DIM))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __table_args__ = (
        Index(
            "supplier_supplier_description_vector_idx",
            supplier_description_vector,
            postgresql_using="hnsw",
            postgresql_with={"m": 32, "ef_construction": 100},
            postgresql_ops={"supplier_description_vector": "vector_cosine_ops"}
        ),
    )
