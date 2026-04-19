"""Unit tests for grade manager."""

from __future__ import annotations

from student_grade_pkg.grade_manager import GradeManager
from student_grade_pkg.student_manager import StudentManager


def test_add_and_get_student_grades(
    student_manager: StudentManager,
    grade_manager: GradeManager,
) -> None:
    """Grades should be added and retrieved."""
    student_manager.add_student("S001", "Raj Kumar")
    assert grade_manager.add_grade("S001", "Maths", "Test", 85, 1) is True
    assert grade_manager.add_grade("S001", "English", "Test", 75, 1) is True

    assert grade_manager.get_student_grades("S001") == [
        ("Maths", "Test", 85, 1),
        ("English", "Test", 75, 1),
    ]


def test_average_calculation(
    student_manager: StudentManager,
    grade_manager: GradeManager,
) -> None:
    """Average should be computed correctly."""
    student_manager.add_student("S001", "Raj Kumar")
    grade_manager.add_grade("S001", "Maths", "Test", 90, 1)
    grade_manager.add_grade("S001", "Science", "Test", 70, 1)

    assert grade_manager.get_average("S001") == 80.0


def test_get_by_semester(
    student_manager: StudentManager,
    grade_manager: GradeManager,
) -> None:
    """Semester filter should only return matching rows."""
    student_manager.add_student("S001", "Raj Kumar")
    grade_manager.add_grade("S001", "Maths", "Test", 88, 1)
    grade_manager.add_grade("S001", "Maths", "Test", 91, 2)

    assert grade_manager.get_by_semester("S001", 1) == [("Maths", "Test", 88)]


def test_invalid_and_error_conditions(
    student_manager: StudentManager,
    grade_manager: GradeManager,
) -> None:
    """Invalid grade data and missing student should fail gracefully."""
    student_manager.add_student("S001", "Raj Kumar")
    assert grade_manager.add_grade("S999", "Maths", "Test", 80, 1) is False
    assert grade_manager.add_grade("S001", "Maths", "Test", 101, 1) is False
    assert grade_manager.get_by_semester("S001", 0) == []
