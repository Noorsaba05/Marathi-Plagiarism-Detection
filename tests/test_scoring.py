# tests/test_scoring.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic.scoring_engine import WeightedScoringEngine

def test_scoring_engine():
    engine = WeightedScoringEngine()

    print("=== Weighted Scoring Engine Test ===\n")

    # Test cases from our viva discussion
    test_cases = [
        {
            "label": "High monolingual, low cross-lang (your viva example)",
            "monolingual_score": 0.90,
            "cross_lang_score": 0.50
        },
        {
            "label": "Both scores high (clear plagiarism)",
            "monolingual_score": 0.95,
            "cross_lang_score": 0.98
        },
        {
            "label": "Both scores low (original content)",
            "monolingual_score": 0.15,
            "cross_lang_score": 0.10
        },
        {
            "label": "Borderline case",
            "monolingual_score": 0.85,
            "cross_lang_score": 0.78
        },
    ]

    for case in test_cases:
        result = engine.compute_final_score(
            case["monolingual_score"],
            case["cross_lang_score"]
        )
        print(f"Case    : {case['label']}")
        print(f"Mono    : {result['monolingual_score']} × 0.6 = "
              f"{round(result['monolingual_score'] * 0.6, 4)}")
        print(f"Cross   : {result['cross_lang_score']} × 0.4 = "
              f"{round(result['cross_lang_score'] * 0.4, 4)}")
        print(f"Final   : {result['final_score']}")
        print(f"Flagged : {result['is_plagiarised']}")
        print(f"Verdict : {result['verdict']}")
        print()

    # Document-level test
    print("=== Document Level Scoring Test ===\n")
    document_sentences = [
        {
            "sentence": "भारत हा एक लोकशाही देश आहे",
            "matched_source": "India is a democratic country",
            "monolingual_score": 0.95,
            "cross_lang_score": 0.99
        },
        {
            "sentence": "शिक्षण समाजाचा पाया आहे",
            "matched_source": "Education is the foundation of society",
            "monolingual_score": 0.88,
            "cross_lang_score": 0.91
        },
        {
            "sentence": "आज हवामान छान आहे",
            "matched_source": "",
            "monolingual_score": 0.12,
            "cross_lang_score": 0.08
        },
    ]

    doc_result = engine.score_document(document_sentences)
    print(f"Total sentences    : {doc_result['total_sentences']}")
    print(f"Flagged sentences  : {doc_result['flagged_sentences']}")
    print(f"Plagiarism %       : {doc_result['plagiarism_percentage']}%")
    print(f"Document verdict   : {doc_result['document_verdict']}")
    print("\nPer-sentence breakdown:")
    for s in doc_result['sentence_scores']:
        print(f"  [{s['final_score']}] {s['verdict']}")
        print(f"       {s['sentence']}")

if __name__ == "__main__":
    test_scoring_engine()