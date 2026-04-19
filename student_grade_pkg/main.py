"""Application entry point for sample usage."""

from __future__ import annotations

from .database import create_database
from .grade_manager import GradeManager
from .student_manager import StudentManager


def main() -> None:
    """Run a small demonstration of the package features."""
    create_database()

    student_mgr = StudentManager()
    grade_mgr = GradeManager()

    student_mgr.add_student("S001", "Raj Kumar")
    student_mgr.add_student("S002", "Priya Singh")

    grade_mgr.add_grade("S001", "Maths", "Test", 85, 1)
    grade_mgr.add_grade("S001", "English", "Test", 78, 1)
    grade_mgr.add_grade("S002", "Maths", "Test", 92, 1)

    print("S001 Grades:", grade_mgr.get_student_grades("S001"))
    print("S001 Average:", grade_mgr.get_average("S001"))
    print("S001 Semester 1:", grade_mgr.get_by_semester("S001", 1))


if __name__ == "__main__":
    main()
