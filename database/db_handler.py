# database/db_handler.py

import sqlite3
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class DatabaseHandler:
    """
    Handles all SQLite database operations.
    Stores submission history and plagiarism reports.
    """

    def __init__(self):
        self.db_path = config.DB_PATH
        self._initialize_db()

    def _initialize_db(self):
        """
        Creates database tables if they don't exist.
        Called automatically on first run.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                submitted_at TEXT NOT NULL,
                total_sentences INTEGER,
                flagged_sentences INTEGER,
                plagiarism_percentage REAL,
                document_verdict TEXT,
                full_report TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"[DB] Database ready at: {self.db_path}")

    def save_report(self, filename: str, report: dict) -> int:
        """
        Save a plagiarism report to the database.
        Returns the submission ID.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO submissions (
                filename,
                submitted_at,
                total_sentences,
                flagged_sentences,
                plagiarism_percentage,
                document_verdict,
                full_report
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            report.get("total_sentences", 0),
            report.get("flagged_sentences", 0),
            report.get("plagiarism_percentage", 0.0),
            report.get("document_verdict", ""),
            json.dumps(report, ensure_ascii=False)
        ))

        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"[DB] Report saved with ID: {submission_id}")
        return submission_id

    def get_all_submissions(self) -> list:
        """
        Retrieve all past submissions for the history page.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, filename, submitted_at,
                   plagiarism_percentage, document_verdict
            FROM submissions
            ORDER BY submitted_at DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "filename": r[1],
                "submitted_at": r[2],
                "plagiarism_percentage": r[3],
                "document_verdict": r[4]
            }
            for r in rows
        ]

    def get_report_by_id(self, submission_id: int) -> dict:
        """
        Retrieve full report for a specific submission.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT full_report FROM submissions WHERE id = ?',
            (submission_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return {}