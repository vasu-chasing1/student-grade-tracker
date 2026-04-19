"""Application settings and configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the application."""

    BASE_DIR: Path
    PACKAGE_DIR: Path
    DEFAULT_DB_FILENAME: str
    DB_PATH: str
    LOG_LEVEL: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings object."""
    base_dir = Path(__file__).resolve().parent.parent
    package_dir = base_dir / "student_grade_pkg"
    db_filename = os.getenv("SGT_DB_FILENAME", "grades.db")
    db_path = os.getenv("SGT_DB_PATH", str(package_dir / db_filename))
    log_level = os.getenv("SGT_LOG_LEVEL", "INFO")

    return Settings(
        BASE_DIR=base_dir,
        PACKAGE_DIR=package_dir,
        DEFAULT_DB_FILENAME=db_filename,
        DB_PATH=db_path,
        LOG_LEVEL=log_level,
    )
