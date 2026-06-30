# tests/test_cross_language.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic.embedder import MarathiEmbedder
from semantic.similarity_engine import SimilarityEngine
from cross_language.translation_detector import CrossLanguageDetector

def test_cross_language_detection():

    embedder = MarathiEmbedder()
    engine = SimilarityEngine(embedder.get_embedding_dimension())
    detector = CrossLanguageDetector(embedder, engine)

    # English reference corpus
    english_corpus = [
        "India is a democratic country with a federal structure",
        "Education is the foundation of social development",
        "Science and technology play a vital role in national progress",
        "The constitution of India guarantees fundamental rights to citizens",
    ]

    detector.build_english_corpus(english_corpus)

    # Marathi translations of above — simulating student plagiarism
    suspicious_sentences = [
        "भारत हे एक लोकशाही राष्ट्र आहे ज्याची संघराज्य रचना आहे",
        "शिक्षण हा सामाजिक विकासाचा पाया आहे",
    ]

    print("\n=== Cross-Language Plagiarism Detection Test ===")
    results = detector.detect(suspicious_sentences)

    print("\n=== Final Results ===")
    for r in results:
        print(f"\nMarathi  : {r['original_marathi']}")
        print(f"English  : {r['translated_english']}")
        print(f"Flagged  : {r['is_cross_lang_plagiarised']}")
        print(f"Top match: {r['top_matches'][0]['sentence']}")
        print(f"Score    : {r['top_matches'][0]['similarity_score']:.4f}")

if __name__ == "__main__":
    test_cross_language_detection()