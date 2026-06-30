# semantic/scoring_engine.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class WeightedScoringEngine:
    """
    Combines monolingual and cross-language scores into a
    single final similarity score as defined in paper Section 4.4.

    Formula:
        Final Score = (0.6 × monolingual_score) + (0.4 × cross_language_score)
        Exception: If cross_lang_score < 0.3, use monolingual_score directly.
    """

    def __init__(self):
        self.w_mono = 0.6
        self.w_cross = 0.4
        self.threshold = config.SEMANTIC_SIMILARITY_THRESHOLD

    def compute_final_score(
        self,
        monolingual_score: float,
        cross_lang_score: float
    ) -> dict:
        """
        Compute weighted final score for a single sentence.
        If cross_lang_score is negligible, use monolingual score directly.
        """
        if cross_lang_score < 0.6:
            final_score = monolingual_score
        else:
            final_score = (
                (self.w_mono * monolingual_score) +
                (self.w_cross * cross_lang_score)
            )

        final_score = min(final_score, 1.0)

        return {
            "monolingual_score": round(monolingual_score, 4),
            "cross_lang_score": round(cross_lang_score, 4),
            "final_score": round(final_score, 4),
            "is_plagiarised": final_score >= self.threshold,
            "verdict": self._get_verdict(final_score)
        }

    def _get_verdict(self, score: float) -> str:
        """Human-readable verdict for the XAI interface."""
        if score >= 0.90:
            return "High Risk — Very likely plagiarised"
        elif score >= 0.82:
            return "Flagged — Probable plagiarism, review recommended"
        elif score >= 0.65:
            return "Suspicious — Manual review suggested"
        elif score >= 0.40:
            return "Low similarity — Unlikely plagiarism"
        else:
            return "Original — No significant match found"

    def score_document(self, sentence_results: list) -> dict:
        """
        Score an entire document by aggregating sentence scores.

        Args:
            sentence_results: List of dicts each containing:
                - sentence: Marathi sentence text
                - monolingual_score: float
                - cross_lang_score: float
                - matched_source: str
        """
        scored_sentences = []
        flagged_count = 0

        for item in sentence_results:
            score_result = self.compute_final_score(
                monolingual_score=item.get("monolingual_score", 0.0),
                cross_lang_score=item.get("cross_lang_score", 0.0)
            )

            scored_sentences.append({
                "sentence": item.get("sentence", ""),
                "matched_source": item.get("matched_source", ""),
                **score_result
            })

            if score_result["is_plagiarised"]:
                flagged_count += 1

        total = len(scored_sentences)
        plagiarism_percentage = (
            round((flagged_count / total) * 100, 2) if total > 0 else 0.0
        )

        if plagiarism_percentage >= 40:
            doc_verdict = "High plagiarism detected"
        elif plagiarism_percentage >= 20:
            doc_verdict = "Moderate plagiarism detected"
        elif plagiarism_percentage >= 5:
            doc_verdict = "Low plagiarism detected"
        else:
            doc_verdict = "Document appears original"

        return {
            "total_sentences": total,
            "flagged_sentences": flagged_count,
            "plagiarism_percentage": plagiarism_percentage,
            "document_verdict": doc_verdict,
            "sentence_scores": scored_sentences
        }