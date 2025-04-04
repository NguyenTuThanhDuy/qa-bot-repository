from typing import List

from sqlalchemy import Integer, Text, DateTime, func, Table, ForeignKey, Column, text, Boolean
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.schema import Index
from sqlalchemy.sql.expression import literal, cast
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
        Index(
            "qa_history_input_text_gin_idx",
            text("to_tsvector('simple', input_text)"),
            postgresql_using="gin"
        ),
    )

    @classmethod
    def prepare_sql_stmt(cls):
        """
        <=> - Cosine Distance = 1 - Cosine Similarity (Low distance means they are similar)
        """
        return """
            SELECT 
                qa_id,
                input_text, 1 - (embedded_vector <=> CAST(:query_vector AS Vector)) AS similarity
            FROM
                qa_history
            WHERE
                embedded_vector <=> CAST(:query_vector AS Vector) < :cosine_distance OR
                to_tsvector('simple', input_text) @@ plainto_tsquery(:text_query)
            ORDER BY 
                similarity DESC
            LIMIT :limit
        """


product_supplier_association = Table(
    "product_supplier",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True),
    Column("supplier_id", Integer, ForeignKey("supplier.supplier_id", ondelete="CASCADE"), primary_key=True),
)


collection_product_association = Table(
    "collection_product",
    Base.metadata,
    Column("collection_id", Integer, ForeignKey("collection.collection_id", ondelete="CASCADE"), primary_key=True),
    Column("product_id", Integer, ForeignKey("product.product_id", ondelete="CASCADE"), primary_key=True),
)


class Brand(Base):
    __tablename__ = "brand"

    brand_id: Mapped[int] = mapped_column(Integer, name="brand_id", primary_key=True, autoincrement=True)
    brand_name: Mapped[str] = mapped_column(Text, name="brand_name", unique=True, nullable=False)
    brand_description: Mapped[str] = mapped_column(Text, name="brand_description")
    is_active: Mapped[bool] = mapped_column(Boolean, name="is_active", default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    # One-to-Many Relationship (Brand → Products)
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="brand",
        cascade="all, delete"
    )


class Collection(Base):
    __tablename__ = "collection"

    collection_id: Mapped[int] = mapped_column(Integer, name="collection_id", primary_key=True, autoincrement=True)
    collection_name: Mapped[str] = mapped_column(Text, name="collection_name", unique=True)
    collection_description: Mapped[str] = mapped_column(Text, name="collection_description")
    is_active: Mapped[bool] = mapped_column(Boolean, name="is_active", default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    products: Mapped[List["Product"]] = relationship(
        "Product",
        secondary=collection_product_association,
        back_populates="collections"
    )


class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(Integer, name="product_id", primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(Text, name="product_name", unique=True)
    product_description: Mapped[str] = mapped_column(Text, name="product_description")
    product_description_vector: Mapped[List[float]] = mapped_column(Vector(N_DIM))
    is_active: Mapped[bool] = mapped_column(Boolean, name="is_active", default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    suppliers: Mapped[List["Supplier"]] = relationship(
        "Supplier",
        secondary=product_supplier_association,
        back_populates="products",
        cascade="all, delete"
    )

    collections: Mapped[List["Collection"]] = relationship(
        "Collection",
        secondary=collection_product_association,
        back_populates="products",
        cascade="all, delete"
    )

    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brand.brand_id", ondelete="CASCADE"), nullable=False)
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")

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
    is_active: Mapped[bool] = mapped_column(Boolean, name="is_active", default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())

    products: Mapped[List["Product"]] = relationship(
        "Product",
        secondary=product_supplier_association,
        back_populates="suppliers"
    )
