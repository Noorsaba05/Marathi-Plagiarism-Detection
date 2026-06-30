# build_academic_corpus.py
# Builds academic Marathi corpus from Marathi Wikipedia via HuggingFace

import json
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing.marathi_preprocessor import MarathiPreprocessor


def is_good_sentence(sentence: str) -> bool:
    """
    Filter criteria for academic quality sentences.
    """
    if len(sentence) < 30 or len(sentence) > 300:
        return False

    devanagari = len(re.findall(r'[\u0900-\u097F]', sentence))
    total = len(sentence.replace(' ', ''))

    if total == 0 or (devanagari / total) < 0.70:
        return False

    if len(sentence.split()) < 4:
        return False

    return True


def build_academic_corpus():
    print("[Corpus] Loading Marathi Wikipedia from HuggingFace...")

    from datasets import load_dataset

    dataset = load_dataset(
        'wikimedia/wikipedia',
        '20231101.mr',
        streaming=True,
        split='train'
    )

    preprocessor = MarathiPreprocessor()
    marathi_sentences = []
    target = 500
    checked = 0
    max_articles = 200

    print(f"[Corpus] Collecting {target} quality sentences "
          f"from up to {max_articles} Wikipedia articles...")

    for item in dataset:
        if checked >= max_articles or len(marathi_sentences) >= target:
            break

        checked += 1
        text = item.get("text", "").strip()

        if not text:
            continue

        # Split into sentences
        segments = re.split(r'[।\.]\s*', text)
        for segment in segments:
            segment = segment.strip()
            if is_good_sentence(segment):
                marathi_sentences.append(segment)
                if len(marathi_sentences) >= target:
                    break

        if checked % 50 == 0:
            print(f"[Corpus] Articles: {checked} | "
                  f"Sentences: {len(marathi_sentences)}")

    print(f"\n[Corpus] Collected {len(marathi_sentences)} sentences "
          f"from {checked} articles")

    # Load existing corpus
    with open("corpus_data.json", "r", encoding="utf-8") as f:
        existing = json.load(f)

    english_sentences = existing["english"]
    existing_marathi = existing["marathi"]

    # Merge and deduplicate
    all_marathi = list(set(existing_marathi + marathi_sentences))
    print(f"[Corpus] Total after merge: {len(all_marathi)} sentences")

    # Save
    corpus = {
        "marathi": all_marathi,
        "english": english_sentences
    }

    with open("corpus_data.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)

    print("[Corpus] corpus_data.json updated!")
    print("\n[Preview] Sample Wikipedia sentences:")
    for i, s in enumerate(marathi_sentences[:5]):
        print(f"  [{i+1}] {s}")


if __name__ == "__main__":
    build_academic_corpus()