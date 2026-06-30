# semantic/similarity_engine.py

import numpy as np
import faiss
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class SimilarityEngine:
    """
    Uses FAISS to efficiently find similar sentences.
    
    Why FAISS instead of simple cosine similarity loop?
    - A loop comparing every sentence pair is O(n²) — slow
    - FAISS uses Approximate Nearest Neighbor search — O(log n)
    - At scale (10,000 sentences), FAISS is 100x faster
    """

    def __init__(self, embedding_dim: int):
        """
        Initialize a FAISS flat index.
        FlatIP = Flat (exact search) + Inner Product (dot product)
        Since our embeddings are normalized, dot product = cosine similarity
        """
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        
        # Store original sentences alongside their vectors
        self.stored_sentences = []
        
        print(f"[SimilarityEngine] FAISS index created. Dimension: {embedding_dim}")

    def add_to_index(self, sentences: list, embeddings: np.ndarray):
        """
        Add a corpus of sentences and their embeddings to the FAISS index.
        This builds our reference database.
        """
        # FAISS requires float32 specifically
        embeddings = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings)
        self.stored_sentences.extend(sentences)
        
        print(f"[SimilarityEngine] Added {len(sentences)} sentences to index.")
        print(f"[SimilarityEngine] Total sentences in index: {self.index.ntotal}")

    def find_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        """
        Given a query sentence embedding, find the top_k most similar
        sentences in our corpus index.
        
        Returns a list of dicts with sentence text and similarity score.
        """
        # Reshape to 2D array as FAISS expects (1, embedding_dim)
        query = np.array([query_embedding]).astype('float32')
        
        # Search the index
        # D = distances (similarity scores), I = indices
        distances, indices = self.index.search(query, top_k)
        
        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx == -1:  # FAISS returns -1 if not enough results
                continue
            results.append({
                "sentence": self.stored_sentences[idx],
                "similarity_score": float(score),
                "is_plagiarised": float(score) >= config.SEMANTIC_SIMILARITY_THRESHOLD
            })
        
        return results

    def get_index_size(self) -> int:
        """Returns total number of sentences currently indexed."""
        return self.index.ntotal