"""Simple in-memory embedding store using FAISS."""

from __future__ import annotations

from typing import List

import faiss
import numpy as np


class EmbeddingStore:
    def __init__(self, dim: int) -> None:
        self.index = faiss.IndexFlatL2(dim)
        self.vectors: List[str] = []

    def add(self, vector: np.ndarray, payload: str) -> None:
        self.index.add(vector.astype("float32"))
        self.vectors.append(payload)

    def search(self, vector: np.ndarray, k: int = 5) -> List[str]:
        distances, indices = self.index.search(vector.astype("float32"), k)
        return [self.vectors[i] for i in indices[0] if i < len(self.vectors)]
