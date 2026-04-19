"""Unit tests for student manager."""

from __future__ import annotations

from student_grade_pkg.student_manager import StudentManager


def test_add_and_get_student(student_manager: StudentManager) -> None:
    """Student should be inserted and retrieved."""
    assert student_manager.add_student("S001", "Raj Kumar") is True
    assert student_manager.get_student("S001") == ("S001", "Raj Kumar")


def test_get_all_students(student_manager: StudentManager) -> None:
    """All added students should be returned."""
    student_manager.add_student("S001", "Raj Kumar")
    student_manager.add_student("S002", "Priya Singh")

    assert student_manager.get_all_students() == [
        ("S001", "Raj Kumar"),
        ("S002", "Priya Singh"),
    ]


def test_duplicate_student_fails(student_manager: StudentManager) -> None:
    """Duplicate student id should fail gracefully."""
    assert student_manager.add_student("S001", "Raj Kumar") is True
    assert student_manager.add_student("S001", "Raj Kumar") is False


def test_invalid_student_input(student_manager: StudentManager) -> None:
    """Invalid student values should be rejected."""
    assert student_manager.add_student("", "Name") is False
    assert student_manager.add_student("S001", "") is False
