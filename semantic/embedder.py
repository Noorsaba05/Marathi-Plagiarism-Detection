# semantic/embedder.py

import sys
import os
import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class MarathiEmbedder:
    """
    Converts Marathi sentences into semantic vector embeddings
    using MahaSBERT — a Sentence-BERT model fine-tuned specifically
    on Marathi sentence pairs.

    Why MahaSBERT over a generic multilingual model?
    - Trained on Marathi NLI (Natural Language Inference) pairs
    - Optimized for SENTENCE-level similarity, not word-level
    - Understands Marathi paraphrasing patterns specifically
    """

    def __init__(self):
        print(f"[Embedder] Loading model: {config.EMBEDDING_MODEL}")
        print("[Embedder] First load will download the model (~400MB). Please wait...")
        
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        print(f"[Embedder] Model loaded. Embedding dimension: {self.embedding_dim}")

    def embed_sentence(self, sentence: str) -> np.ndarray:
        """
        Convert a single Marathi sentence into a vector.
        Returns a 1D numpy array of shape (embedding_dim,)
        """
        embedding = self.model.encode(
            sentence,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalizing makes cosine similarity
                                       # equivalent to dot product — faster
        )
        return embedding

    def embed_sentences(self, sentences: list) -> np.ndarray:
        """
        Convert a list of sentences into a matrix of vectors.
        Returns a 2D numpy array of shape (num_sentences, embedding_dim)
        
        Uses batch processing — much faster than one by one.
        """
        if not sentences:
            return np.array([])

        embeddings = self.model.encode(
            sentences,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=32,        # Process 32 sentences at a time
            show_progress_bar=True
        )
        return embeddings

    def get_embedding_dimension(self) -> int:
        """Returns the vector size — useful when building FAISS index."""
        return self.embedding_dim