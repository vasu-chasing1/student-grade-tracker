"""Database setup utilities."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from config.settings import get_settings
from .utils import get_logger

logger = get_logger(__name__)


def create_database(db_path: Optional[str] = None) -> str:
    """Create required database tables if they do not exist.

    Args:
        db_path: Optional custom database path.

    Returns:
        Resolved database path as a string.

    Raises:
        sqlite3.Error: If database initialization fails.
    """
    settings = get_settings()
    resolved_path = Path(db_path) if db_path else Path(settings.DB_PATH)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(resolved_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS students(
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS grades(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    grade_type TEXT NOT NULL,
                    grade_value INTEGER NOT NULL,
                    semester INTEGER NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                )
                """
            )
            conn.commit()
        logger.info("Database initialized successfully at %s", resolved_path)
    except sqlite3.Error:
        logger.exception("Error creating database at %s", resolved_path)
        raise

    return str(resolved_path)
