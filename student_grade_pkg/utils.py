"""Shared utility helpers."""

from __future__ import annotations

import logging
from typing import Any

from config.settings import get_settings


def get_logger(name: str) -> logging.Logger:
    """Create and configure a module logger.

    Args:
        name: Logger name.

    Returns:
        Configured logger instance.
    """
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logging.getLogger(name)


def validate_non_empty(value: str, field_name: str) -> None:
    """Validate non-empty string value.

    Args:
        value: Input value.
        field_name: Name for validation message.

    Raises:
        ValueError: If value is empty.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def validate_grade_value(value: Any) -> None:
    """Validate grade value range.

    Args:
        value: Grade value expected as integer in range 0-100.

    Raises:
        ValueError: If grade value is invalid.
    """
    if not isinstance(value, int) or value < 0 or value > 100:
        raise ValueError("grade_value must be an integer between 0 and 100")


def validate_semester(value: Any) -> None:
    """Validate semester number.

    Args:
        value: Semester value expected as positive integer.

    Raises:
        ValueError: If semester is invalid.
    """
    if not isinstance(value, int) or value <= 0:
        raise ValueError("semester must be a positive integer")
