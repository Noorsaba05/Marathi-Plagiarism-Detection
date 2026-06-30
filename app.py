# app.py

import os
import sys
from flask import Flask, request, jsonify, render_template

# Import all our modules
from preprocessing.marathi_preprocessor import MarathiPreprocessor
from semantic.embedder import MarathiEmbedder
from semantic.similarity_engine import SimilarityEngine
from semantic.scoring_engine import WeightedScoringEngine
from cross_language.translation_detector import CrossLanguageDetector
from database.db_handler import DatabaseHandler
from preprocessing.document_extractor import DocumentExtractor
import tempfile

app = Flask(__name__)

# --- Initialize all modules once at startup ---
print("[App] Initializing system modules...")

preprocessor = MarathiPreprocessor()
embedder = MarathiEmbedder()

# Two separate FAISS indexes — one for Marathi, one for English
marathi_engine = SimilarityEngine(embedder.get_embedding_dimension())
english_engine = SimilarityEngine(embedder.get_embedding_dimension())

scoring_engine = WeightedScoringEngine()
cross_lang_detector = CrossLanguageDetector(embedder, english_engine)
db = DatabaseHandler()

extractor = DocumentExtractor()

# --- Load sample corpus (replace with real corpus in production) ---
print("[App] Loading reference corpus...")

# Load corpus from file built by build_corpus.py
import json

with open("corpus_data.json", "r", encoding="utf-8") as f:
    corpus_data = json.load(f)

MARATHI_CORPUS = [s.rstrip('.') for s in corpus_data["marathi"]]
ENGLISH_CORPUS = corpus_data["english"]

print(f"[App] Loaded {len(MARATHI_CORPUS)} Marathi sentences")
print(f"[App] Loaded {len(ENGLISH_CORPUS)} English sentences")

marathi_embeddings = embedder.embed_sentences(MARATHI_CORPUS)
marathi_engine.add_to_index(MARATHI_CORPUS, marathi_embeddings)

cross_lang_detector.build_english_corpus(ENGLISH_CORPUS)

print("[App] System ready!")


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_plagiarism():
    """
    Main plagiarism detection endpoint.
    Accepts Marathi text via POST, returns full report.
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data['text'].strip()
    filename = data.get('filename', 'manual_input')

    if not input_text:
        return jsonify({"error": "Empty text provided"}), 400

    # Step 1: Preprocess — split on . and । first manually
    import re as _re
    # Split input into individual sentences on . and ।
    raw_sentences = _re.split(r'[।\.]\s*', input_text)
    raw_sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 10]

    sentences = []
    for raw in raw_sentences:
        processed = preprocessor.preprocess(raw)
        if processed['sentences']:
            sentences.extend(processed['sentences'])
        else:
            sentences.append(raw)

    if not sentences:
        return jsonify({"error": "No sentences found after preprocessing"}), 400

    # Step 2 & 3: Score each sentence
    sentence_results = []

    for sentence in sentences:
        # Monolingual check
        mono_embedding = embedder.embed_sentence(sentence)
        mono_matches = marathi_engine.find_similar(mono_embedding, top_k=1)
        mono_score = mono_matches[0]['similarity_score'] if mono_matches else 0.0
        mono_source = mono_matches[0]['sentence'] if mono_matches else ""

        # Cross-language check
        try:
            english = cross_lang_detector.translate_to_english(sentence)
        except Exception:
            english = ""
        cross_score = 0.0
        cross_source = ""

        if english:
            cross_embedding = embedder.embed_sentence(english)
            cross_matches = english_engine.find_similar(cross_embedding, top_k=1)
            cross_score = cross_matches[0]['similarity_score'] if cross_matches else 0.0
            cross_source = cross_matches[0]['sentence'] if cross_matches else ""

        print(f"[DEBUG] Sentence: {sentence[:40]}")
        print(f"[DEBUG] Mono: {mono_score:.4f} | Cross: {cross_score:.4f}")

        sentence_results.append({
            "sentence": sentence,
            "english_translation": english,
            "matched_source": mono_source or cross_source,
            "monolingual_score": mono_score,
            "cross_lang_score": cross_score
        })
            
   # Step 4: Compute weighted scores
    report = scoring_engine.score_document(sentence_results)
    print(f"[DEBUG] sentence_results count: {len(sentence_results)}")
    print(f"[DEBUG] report: {report}")

    # Step 5: Add XAI detail to each sentence
    for i, s in enumerate(report['sentence_scores']):
        if i < len(sentence_results):
            s['english_translation'] = sentence_results[i].get('english_translation', '')
            s['matched_source'] = sentence_results[i].get('matched_source', '')

    # Step 6: Save to database
    submission_id = db.save_report(filename, report)
    report['submission_id'] = submission_id

    return jsonify(report)


@app.route('/report/<int:submission_id>')
def get_report(submission_id):
    """Return full report for a specific submission."""
    report = db.get_report_by_id(submission_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report)

@app.route('/upload', methods=['POST'])
def upload_document():
    """
    File upload endpoint.
    Accepts PDF or DOCX, extracts text, runs plagiarism check.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check allowed extensions
    allowed = {'.pdf', '.docx', '.doc', '.txt'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        return jsonify({
            "error": f"Unsupported file type '{ext}'. "
                     f"Allowed: PDF, DOCX, TXT"
        }), 400

    # Save to temp file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=ext
    ) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Extract text
        print(f"[Upload] Extracting text from: {file.filename}")
        text = extractor.extract(tmp_path)

        if not text:
            return jsonify({
                "error": "Could not extract text from file. "
                         "Ensure the file contains readable text."
            }), 400

        print(f"[Upload] Extracted {len(text)} characters")

        # Split into sentences
        import re as _re
        raw_sentences = _re.split(r'[।\.]\s*', text)
        raw_sentences = [s.strip() for s in raw_sentences
                        if len(s.strip()) > 10]

        sentences = []
        for raw in raw_sentences:
            processed = preprocessor.preprocess(raw)
            if processed['sentences']:
                sentences.extend(processed['sentences'])
            else:
                sentences.append(raw)

        if not sentences:
            return jsonify({
                "error": "No Marathi sentences found in document."
            }), 400

        # Score each sentence
        sentence_results = []
        for sentence in sentences:
            mono_embedding = embedder.embed_sentence(sentence)
            mono_matches = marathi_engine.find_similar(
                mono_embedding, top_k=1
            )
            mono_score = (mono_matches[0]['similarity_score']
                         if mono_matches else 0.0)
            mono_source = (mono_matches[0]['sentence']
                          if mono_matches else "")

            try:
                english = cross_lang_detector.translate_to_english(sentence)
            except Exception:
                english = ""

            cross_score = 0.0
            cross_source = ""

            if english:
                cross_embedding = embedder.embed_sentence(english)
                cross_matches = english_engine.find_similar(
                    cross_embedding, top_k=1
                )
                cross_score = (cross_matches[0]['similarity_score']
                              if cross_matches else 0.0)
                cross_source = (cross_matches[0]['sentence']
                               if cross_matches else "")

            sentence_results.append({
                "sentence": sentence,
                "english_translation": english,
                "matched_source": mono_source or cross_source,
                "monolingual_score": mono_score,
                "cross_lang_score": cross_score
            })

        # Score document
        report = scoring_engine.score_document(sentence_results)

        for i, s in enumerate(report['sentence_scores']):
            if i < len(sentence_results):
                s['english_translation'] = sentence_results[i].get(
                    'english_translation', ''
                )
                s['matched_source'] = sentence_results[i].get(
                    'matched_source', ''
                )

        # Save to database
        submission_id = db.save_report(file.filename, report)
        report['submission_id'] = submission_id
        report['filename'] = file.filename

        return jsonify(report)

    finally:
        # Clean up temp file
        os.unlink(tmp_path)
        
if __name__ == '__main__':
    app.run(debug=True, port=5000)