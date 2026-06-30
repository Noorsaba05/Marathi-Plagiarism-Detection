# preprocessing/document_extractor.py

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DocumentExtractor:
    """
    Extracts plain text from PDF and DOCX files.
    Supports Marathi Unicode text in both formats.
    """

    def extract(self, filepath: str) -> str:
        """
        Auto-detect file type and extract text.
        Returns plain text string.
        """
        ext = os.path.splitext(filepath)[1].lower()

        if ext == '.pdf':
            return self._extract_pdf(filepath)
        elif ext in ['.docx', '.doc']:
            return self._extract_docx(filepath)
        elif ext == '.txt':
            return self._extract_txt(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _extract_pdf(self, filepath: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            print(f"[Extractor] PDF error: {e}")
            return ""

    def _extract_docx(self, filepath: str) -> str:
        """Extract text from DOCX using python-docx."""
        try:
            from docx import Document
            doc = Document(filepath)
            text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text.strip() + "\n"
            return text.strip()
        except Exception as e:
            print(f"[Extractor] DOCX error: {e}")
            return ""

    def _extract_txt(self, filepath: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"[Extractor] TXT error: {e}")
            return ""