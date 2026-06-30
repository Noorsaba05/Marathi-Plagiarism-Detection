# tests/test_preprocessor.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.marathi_preprocessor import MarathiPreprocessor

def test_preprocessor():
    preprocessor = MarathiPreprocessor()

    # Sample Marathi academic text
    sample_text = """भारत हा एक लोकशाही देश आहे। 
    येथे अनेक भाषा बोलल्या जातात। 
    मराठी ही महाराष्ट्राची अधिकृत भाषा आहे।"""

    result = preprocessor.preprocess(sample_text)

    print("=== Preprocessing Test ===")
    print(f"Original:\n{result['original']}")
    print(f"\nNormalized:\n{result['normalized']}")
    print(f"\nCleaned:\n{result['cleaned']}")
    print(f"\nSentences:")
    for i, s in enumerate(result['sentences']):
        print(f"  [{i+1}] {s}")
    print(f"\nTokenized Sentences:")
    for i, tokens in enumerate(result['tokenized_sentences']):
        print(f"  [{i+1}] {tokens}")

    print(f"\nFiltered Sentences (stop words removed):")
    for i, tokens in enumerate(result['filtered_sentences']):
        print(f"  [{i+1}] {tokens}")

if __name__ == "__main__":
    test_preprocessor()