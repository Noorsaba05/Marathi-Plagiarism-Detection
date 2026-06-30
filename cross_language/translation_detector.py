# cross_language/translation_detector.py

import requests
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class CrossLanguageDetector:
    """
    Detects plagiarism from English sources by:
    1. Translating submitted Marathi text back to English
    2. Comparing the English result against English corpus
    """

    def __init__(self, embedder, similarity_engine):
        self.embedder = embedder
        self.engine = similarity_engine
        self.translate_url = "https://translate.googleapis.com/translate_a/single"

    def translate_to_english(self, marathi_text: str) -> str:
        """
        Translates Marathi text to English using Google Translate.
        Note: Production system should use IndicTrans2 for better
        accuracy on academic Marathi text.
        """
        params = {
            "client": "gtx",
            "sl": "mr",
            "tl": "en",
            "dt": "t",
            "q": marathi_text
        }
        try:
            response = requests.get(
                self.translate_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            translated = ""
            for segment in result[0]:
                if segment[0]:
                    translated += segment[0]
            return translated.strip()
        except requests.exceptions.Timeout:
            print("[CrossLang] Translation request timed out.")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"[CrossLang] Translation error: {e}")
            return ""

    def build_english_corpus(self, english_sentences: list):
        """
        Index English reference sentences into FAISS.
        """
        if not english_sentences:
            print("[CrossLang] Warning: Empty English corpus.")
            return
        print(f"[CrossLang] Building English corpus with "
              f"{len(english_sentences)} sentences...")
        embeddings = self.embedder.embed_sentences(english_sentences)
        self.engine.add_to_index(english_sentences, embeddings)
        print("[CrossLang] English corpus indexed successfully.")

    def detect(self, marathi_sentences: list) -> list:
        """
        Main detection pipeline.
        Translates each Marathi sentence to English,
        then checks against the English corpus.
        """
        results = []
        for i, sentence in enumerate(marathi_sentences):
            print(f"\n[CrossLang] Processing sentence "
                  f"{i+1}/{len(marathi_sentences)}")
            print(f"  Marathi : {sentence}")

            english = self.translate_to_english(sentence)
            if not english:
                print("  [Skip] Translation failed.")
                continue

            print(f"  English : {english}")

            embedding = self.embedder.embed_sentence(english)
            matches = self.engine.find_similar(embedding, top_k=3)

            is_flagged = any(
                m["similarity_score"] >= config.CROSS_LANG_THRESHOLD
                for m in matches
            )

            results.append({
                "original_marathi": sentence,
                "translated_english": english,
                "top_matches": matches,
                "is_cross_lang_plagiarised": is_flagged
            })

            time.sleep(0.5)

        return results