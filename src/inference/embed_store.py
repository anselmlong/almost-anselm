"""FAISS / vector store creation and simple search placeholder.
"""

from typing import List


class EmbedStore:
    def __init__(self, path: str = None):
        self.path = path

    def build(self, embeddings: List[List[float]], ids: List[str]):
        print("Building vector index (placeholder)")

    def search(self, query_emb, k: int = 5):
        return []


if __name__ == "__main__":
    print("EmbedStore placeholder")
