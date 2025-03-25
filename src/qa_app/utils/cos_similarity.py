import numpy as np


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes the cosine similarity between two vectors.
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
