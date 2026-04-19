"""Student management operations."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

from config.settings import get_settings
from .utils import get_logger, validate_non_empty

logger = get_logger(__name__)
StudentRow = Tuple[str, str]


class StudentManager:
    """Manage student records in the SQLite database."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize student manager.

        Args:
            db_path: Optional custom database path.
        """
        settings = get_settings()
        self.db_path = str(Path(db_path) if db_path else Path(settings.DB_PATH))

    def _get_connection(self) -> sqlite3.Connection:
        """Create a database connection with foreign keys enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def add_student(self, student_id: str, name: str) -> bool:
        """Add a new student.

        Args:
            student_id: Unique student identifier.
            name: Student full name.

        Returns:
            True when inserted, else False.
        """
        try:
            validate_non_empty(student_id, "student_id")
            validate_non_empty(name, "name")
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO students (student_id, name) VALUES (?, ?)",
                    (student_id.strip(), name.strip()),
                )
                conn.commit()
            logger.info("Student %s added successfully", student_id)
            return True
        except ValueError:
            logger.exception("Validation error while adding student")
            return False
        except sqlite3.IntegrityError:
            logger.error("Student with ID %s already exists", student_id)
            return False
        except sqlite3.Error:
            logger.exception("Error adding student")
            return False

    def get_student(self, student_id: str) -> Optional[StudentRow]:
        """Fetch a student by ID."""
        try:
            validate_non_empty(student_id, "student_id")
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT student_id, name FROM students WHERE student_id = ?",
                    (student_id.strip(),),
                )
                student = cursor.fetchone()
            return student if student else None
        except ValueError:
            logger.exception("Validation error while fetching student")
            return None
        except sqlite3.Error:
            logger.exception("Error fetching student")
            return None

    def get_all_students(self) -> List[StudentRow]:
        """Return all students."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("SELECT student_id, name FROM students ORDER BY student_id")
                return cursor.fetchall()
        except sqlite3.Error:
            logger.exception("Error fetching all students")
            return []

    def update_student(self, student_id: str, name: str) -> bool:
        """Update student name by ID."""
        try:
            validate_non_empty(student_id, "student_id")
            validate_non_empty(name, "name")
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE students SET name = ? WHERE student_id = ?",
                    (name.strip(), student_id.strip()),
                )
                conn.commit()
            return cursor.rowcount > 0
        except ValueError:
            logger.exception("Validation error while updating student")
            return False
        except sqlite3.Error:
            logger.exception("Error updating student")
            return False

    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID."""
        try:
            validate_non_empty(student_id, "student_id")
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM students WHERE student_id = ?",
                    (student_id.strip(),),
                )
                conn.commit()
            return cursor.rowcount > 0
        except ValueError:
            logger.exception("Validation error while deleting student")
            return False
        except sqlite3.Error:
            logger.exception("Error deleting student")
            return False

        
