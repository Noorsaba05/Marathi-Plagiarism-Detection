# tests/test_scoring_live.py
# Shows us exact scores so we can see what's happening

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.marathi_preprocessor import MarathiPreprocessor
from semantic.embedder import MarathiEmbedder
from semantic.similarity_engine import SimilarityEngine
from semantic.scoring_engine import WeightedScoringEngine
import json

def test_live():
    preprocessor = MarathiPreprocessor()
    embedder = MarathiEmbedder()
    engine = SimilarityEngine(embedder.get_embedding_dimension())
    scoring = WeightedScoringEngine()

    # Load corpus
    with open("corpus_data.json", "r", encoding="utf-8") as f:
        corpus_data = json.load(f)

    marathi_corpus = corpus_data["marathi"]

    # Index corpus
    print("[Test] Indexing corpus...")
    embeddings = embedder.embed_sentences(marathi_corpus)
    engine.add_to_index(marathi_corpus, embeddings)

    # Test sentence — exact copy from corpus
    test_sentences = [
        "भारत हे दक्षिण आशियातील एक प्रजासत्ताक राष्ट्र आहे.",
        "भारत हा जगातील सर्वात मोठा लोकशाही देश आहे.",
        "शिक्षण हे मानवाच्या सर्वांगीण विकासाचे प्रमुख साधन आहे.",
    ]

    print("\n[Test] Checking exact corpus sentences:")
    for sentence in test_sentences:
        embedding = embedder.embed_sentence(sentence)
        matches = engine.find_similar(embedding, top_k=1)
        score = matches[0]['similarity_score'] if matches else 0.0
        matched = matches[0]['sentence'] if matches else ""
        result = scoring.compute_final_score(score, 0.0)
        print(f"\n  Input  : {sentence}")
        print(f"  Match  : {matched}")
        print(f"  Score  : {score:.4f}")
        print(f"  Final  : {result['final_score']}")
        print(f"  Flag   : {result['is_plagiarised']}")
        print(f"  Verdict: {result['verdict']}")

if __name__ == "__main__":
    test_live()