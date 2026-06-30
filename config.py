# config.py
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDIC_NLP_RESOURCES = os.path.join(BASE_DIR, "indic_nlp_resources")
CORPUS_MARATHI = os.path.join(BASE_DIR, "corpus", "marathi_docs")
CORPUS_ENGLISH = os.path.join(BASE_DIR, "corpus", "english_docs")
DB_PATH = os.path.join(BASE_DIR, "plagiarism_records.db")

# Model
EMBEDDING_MODEL = "l3cube-pune/marathi-sentence-bert-nli"

# Thresholds
SEMANTIC_SIMILARITY_THRESHOLD = 0.80
CROSS_LANG_THRESHOLD = 0.75

# Language
MARATHI_LANG_CODE = "mr"