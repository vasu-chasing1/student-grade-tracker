"""Grade management operations."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

from config.settings import get_settings
from .utils import (
    get_logger,
    validate_grade_value,
    validate_non_empty,
    validate_semester,
)

logger = get_logger(__name__)
GradeRow = Tuple[str, str, int, int]
SemesterGradeRow = Tuple[str, str, int]


class GradeManager:
    """Manage grade records in the SQLite database."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize grade manager.

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

    def add_grade(
        self,
        student_id: str,
        subject: str,
        grade_type: str,
        grade_value: int,
        semester: int,
    ) -> bool:
        """Add grade for a student.

        Returns:
            True when inserted, else False.
        """
        try:
            validate_non_empty(student_id, "student_id")
            validate_non_empty(subject, "subject")
            validate_non_empty(grade_type, "grade_type")
            validate_grade_value(grade_value)
            validate_semester(semester)

            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO grades(student_id, subject, grade_type, grade_value, semester)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        student_id.strip(),
                        subject.strip(),
                        grade_type.strip(),
                        grade_value,
                        semester,
                    ),
                )
                conn.commit()
            logger.info("Grade added for %s in %s", student_id, subject)
            return True
        except ValueError:
            logger.exception("Validation error while adding grade")
            return False
        except sqlite3.IntegrityError:
            logger.error("Cannot add grade: student %s does not exist", student_id)
            return False
        except sqlite3.Error:
            logger.exception("Error adding grade")
            return False

    def add_grades(
        self,
        student_id: str,
        subject: str,
        grade_type: str,
        grade_value: int,
        semester: int,
    ) -> bool:
        """Backward-compatible alias for add_grade."""
        return self.add_grade(student_id, subject, grade_type, grade_value, semester)

    def get_student_grades(self, student_id: str) -> List[GradeRow]:
        """Get all grades for a student."""
        try:
            validate_non_empty(student_id, "student_id")
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT subject, grade_type, grade_value, semester
                    FROM grades
                    WHERE student_id = ?
                    ORDER BY id
                    """,
                    (student_id.strip(),),
                )
                return cursor.fetchall()
        except ValueError:
            logger.exception("Validation error while fetching grades")
            return []
        except sqlite3.Error:
            logger.exception("Error fetching grades")
            return []

    def get_average(self, student_id: str) -> float:
        """Get average grade value for a student."""
        try:
            validate_non_empty(student_id, "student_id")
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT AVG(grade_value) FROM grades WHERE student_id = ?",
                    (student_id.strip(),),
                )
                average = cursor.fetchone()
            return float(average[0]) if average and average[0] is not None else 0.0
        except ValueError:
            logger.exception("Validation error while calculating average")
            return 0.0
        except sqlite3.Error:
            logger.exception("Error calculating average")
            return 0.0

    def get_by_semester(self, student_id: str, semester: int) -> List[SemesterGradeRow]:
        """Get grades for a student by semester."""
        try:
            validate_non_empty(student_id, "student_id")
            validate_semester(semester)
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT subject, grade_type, grade_value
                    FROM grades
                    WHERE student_id = ? AND semester = ?
                    ORDER BY id
                    """,
                    (student_id.strip(), semester),
                )
                return cursor.fetchall()
        except ValueError:
            logger.exception("Validation error while fetching semester grades")
            return []
        except sqlite3.Error:
            logger.exception("Error fetching semester grades")
            return []
