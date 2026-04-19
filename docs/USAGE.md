# Usage Guide

## Quick Start

```python
from student_grade_pkg import create_database, StudentManager, GradeManager

db_path = create_database()
students = StudentManager(db_path)
grades = GradeManager(db_path)

students.add_student("S001", "Raj Kumar")
grades.add_grade("S001", "Maths", "Test", 88, 1)

print(grades.get_student_grades("S001"))
print(grades.get_average("S001"))
```

## Configuration

The project supports environment variables:

- `SGT_DB_PATH`: full path to SQLite database
- `SGT_DB_FILENAME`: database filename when `SGT_DB_PATH` is not provided
- `SGT_LOG_LEVEL`: logging level (default: `INFO`)

Example:

```bash
export SGT_DB_PATH=/tmp/custom-grades.db
python run.py
```

## Error Handling Behavior

- Invalid inputs are validated and logged.
- Manager methods return safe defaults (`False`, `None`, `[]`, `0.0`) on errors.
- DB integrity issues (e.g., duplicate student ID) are handled gracefully.
