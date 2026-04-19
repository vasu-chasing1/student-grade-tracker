"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from app import create_app
from student_grade_pkg.database import create_database
from student_grade_pkg.grade_manager import GradeManager
from student_grade_pkg.student_manager import StudentManager


@pytest.fixture()
def db_path(tmp_path: Path) -> str:
    """Provide an isolated SQLite db path."""
    path = tmp_path / "test_grades.db"
    create_database(str(path))
    return str(path)


@pytest.fixture()
def student_manager(db_path: str) -> StudentManager:
    """Provide student manager for isolated db."""
    return StudentManager(db_path)


@pytest.fixture()
def grade_manager(db_path: str) -> GradeManager:
    """Provide grade manager for isolated db."""
    return GradeManager(db_path)


@pytest.fixture()
def app_client(db_path: str):
    """Provide Flask test client for isolated db."""
    app = create_app({"TESTING": True, "DB_PATH": db_path})
    with app.test_client() as client:
        yield client
