from abc import ABC, abstractmethod
import logging

from langchain_openai.embeddings.base import OpenAIEmbeddings
from openai import OpenAIError

from qa_app.utils.text_processor import preprocess_text_decorator


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class IEmbeddingVector(ABC):
    @abstractmethod
    def create_embedding_vector(self, input_text: str):
        raise NotImplementedError()


class EmbeddingVector(IEmbeddingVector):
    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embed = OpenAIEmbeddings(
            model=embedding_model
        )

    @preprocess_text_decorator
    def create_embedding_vector(self, *, input_text: str):
        try:
            embedded_response = self.embed.embed_query(input_text)
            return embedded_response
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError("Error generating embedding vector from OpenAI.") from e
        except Exception as e:
            logger.error(f"Unexpected error while generating embedding: {e}")
            raise RuntimeError("An unexpected error occurred.") from e
