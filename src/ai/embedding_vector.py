from abc import ABC, abstractmethod

import numpy as np

from langchain_openai.embeddings.base import OpenAIEmbeddings

class IEmbeddingVector(ABC):
    @abstractmethod
    def create_embedding_vector(self, input_text: str):
        raise NotImplementedError()


class EmbeddingVector(IEmbeddingVector):
    def __init__(self, embed_model: str = "text-embedding-3-small"):
        self.embed = OpenAIEmbeddings(
            model=embed_model
        )

    def create_embedding_vector(self, input_text):
        return np.array(self.embed.embed_query(input_text))
