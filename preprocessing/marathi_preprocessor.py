# preprocessing/marathi_preprocessor.py

import re
import sys
import os

# Tell IndicNLP where its resources are
from indicnlp import common
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import sentence_tokenize

# Import our central config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize IndicNLP resource path
common.set_resources_path(config.INDIC_NLP_RESOURCES)

class MarathiPreprocessor:
    """
    Handles all text cleaning and tokenization for Marathi text.
    Must be applied to ALL text before embedding or comparison.
    """

    def __init__(self):
        factory = IndicNormalizerFactory()
        self.normalizer = factory.get_normalizer(config.MARATHI_LANG_CODE)
        self.lang = config.MARATHI_LANG_CODE
        self.stop_words = set([
            'आहे', 'आहेत', 'हे', 'हा', 'ही', 'हो', 'ते', 'तो', 'ती',
            'आणि', 'व', 'की', 'पण', 'परंतु', 'तर', 'म्हणून', 'कारण',
            'एक', 'एका', 'या', 'त्या', 'त्यांनी', 'त्यांचे', 'त्याचे',
            'मी', 'तू', 'आम्ही', 'तुम्ही', 'आपण', 'ते', 'त्यांना',
            'काय', 'कसे', 'कोण', 'कुठे', 'केव्हा', 'किती',
            'नाही', 'नव्हते', 'होते', 'होता', 'होती', 'असे', 'असा',
            'च', 'ला', 'ना', 'ने', 'मध्ये', 'वर', 'साठी', 'पासून'
        ])

    def normalize(self, text: str) -> str:
        """
        Step 1: Fix inconsistent Unicode encoding in Devanagari.
        """
        return self.normalizer.normalize(text)

    def remove_noise(self, text: str) -> str:
        """
        Step 2: Remove noise from Marathi text.
        - Removes zero-width characters (evasion attack defense)
        - Removes URLs, English characters, special symbols
        - Keeps only Devanagari characters and spaces
        """
        text = text.replace('\u200d', '')
        text = text.replace('\u200c', '')
        text = re.sub(r'[\u200b\u200e\u200f\ufeff\u00ad]', '', text)
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'[a-zA-Z0-9]', '', text)
        text = re.sub(r'[^\u0900-\u097F\s।.]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def sentence_tokenize(self, text: str) -> list:
        """
        Step 3: Split paragraph into sentences.
        Handles BOTH Marathi sentence boundaries:
        - । (Devanagari danda) used in formal/printed Marathi
        - .  (English full stop) used in digital/typed Marathi
        """
        segments = re.split(r'\.\s+', text)
        sentences = []
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
            sub_sentences = sentence_tokenize.sentence_split(
                segment, lang=self.lang
            )
            sentences.extend(sub_sentences)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def word_tokenize(self, text: str) -> list:
        """
        Step 4: Split sentence into words, remove danda punctuation.
        """
        tokens = indic_tokenize.trivial_tokenize(text, lang=self.lang)
        tokens = [t for t in tokens if t not in ('।', '.')]
        return tokens

    def remove_stop_words(self, tokens: list) -> list:
        """
        Step 5: Remove Marathi stop words from token list.
        """
        return [t for t in tokens if t not in self.stop_words]

    def preprocess(self, text: str) -> dict:
        """
        Master pipeline: runs all steps in order.
        """
        normalized = self.normalize(text)
        cleaned = self.remove_noise(normalized)
        sentences = self.sentence_tokenize(cleaned)
        tokenized_sentences = [
            self.word_tokenize(sentence)
            for sentence in sentences
        ]
        filtered_sentences = [
            self.remove_stop_words(tokens)
            for tokens in tokenized_sentences
        ]
        return {
            "original": text,
            "normalized": normalized,
            "cleaned": cleaned,
            "sentences": sentences,
            "tokenized_sentences": tokenized_sentences,
            "filtered_sentences": filtered_sentences
        }