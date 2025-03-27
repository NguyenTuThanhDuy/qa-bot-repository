from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant

from ai.embedding_vector import EmbeddingVector
from database.config import BaseConfig as Conf


class QdrantConnector(object):
    def __init__(self, collection_name: str, vector_name: str):
        self.qdrant_client = QdrantClient(port=Conf.QDRANT_PORT, host=Conf.QDRANT_HOST)
        self.embedding_vector = EmbeddingVector()
        self.vector_db = Qdrant(
            client=self.qdrant_client,
            embeddings=self.embedding_vector.embed,
            collection_name=collection_name,
            vector_name=vector_name,
        )
