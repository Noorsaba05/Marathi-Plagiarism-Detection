# tests/test_embedder.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.marathi_preprocessor import MarathiPreprocessor
from semantic.embedder import MarathiEmbedder
from semantic.similarity_engine import SimilarityEngine

def test_semantic_pipeline():

    # Step 1: Preprocess
    preprocessor = MarathiPreprocessor()
    embedder = MarathiEmbedder()
    engine = SimilarityEngine(embedder.get_embedding_dimension())

    # --- Build reference corpus (simulating stored academic documents) ---
    corpus_sentences = [
        "भारत हा एक लोकशाही देश आहे",
        "मराठी ही महाराष्ट्राची अधिकृत भाषा आहे",
        "शिक्षण हे समाजाच्या विकासाचे मूळ आहे",
        "विज्ञान आणि तंत्रज्ञान यांचा विकास महत्त्वाचा आहे",
    ]

    print("\n[Test] Building corpus index...")
    corpus_embeddings = embedder.embed_sentences(corpus_sentences)
    engine.add_to_index(corpus_sentences, corpus_embeddings)

    # --- Test 1: Exact match ---
    print("\n[Test 1] Exact match detection:")
    query1 = "भारत हा एक लोकशाही देश आहे"
    q1_embedding = embedder.embed_sentence(query1)
    results1 = engine.find_similar(q1_embedding, top_k=2)
    for r in results1:
        print(f"  Score: {r['similarity_score']:.4f} | "
              f"Plagiarised: {r['is_plagiarised']} | "
              f"Sentence: {r['sentence']}")

    # --- Test 2: Paraphrase detection (the real challenge) ---
    print("\n[Test 2] Paraphrase detection:")
    query2 = "भारत एक प्रजासत्ताक राष्ट्र आहे"  # Same meaning, different words
    q2_embedding = embedder.embed_sentence(query2)
    results2 = engine.find_similar(q2_embedding, top_k=2)
    for r in results2:
        print(f"  Score: {r['similarity_score']:.4f} | "
              f"Plagiarised: {r['is_plagiarised']} | "
              f"Sentence: {r['sentence']}")

    # --- Test 3: Unrelated sentence (should NOT be flagged) ---
    print("\n[Test 3] Unrelated sentence (should not be flagged):")
    query3 = "आज हवामान खूप छान आहे"  # Today the weather is very nice
    q3_embedding = embedder.embed_sentence(query3)
    results3 = engine.find_similar(q3_embedding, top_k=2)
    for r in results3:
        print(f"  Score: {r['similarity_score']:.4f} | "
              f"Plagiarised: {r['is_plagiarised']} | "
              f"Sentence: {r['sentence']}")

if __name__ == "__main__":
    test_semantic_pipeline()