# Student Grade Tracker

A production-ready Python project for managing students and their academic grades using SQLite.

## Features

- Student management (create, update, delete, list)
- Grade management (add, list, filter by semester)
- Average grade calculation
- Flask web dashboard and REST API
- Centralized configuration via `config/settings.py`
- Logging and input validation
- Unit tests with `pytest`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the demo:

```bash
python run.py
```

Run the web app:

```bash
python app/wsgi.py
```

Run tests:

```bash
pytest -q
```

See detailed examples in [`docs/USAGE.md`](docs/USAGE.md).

## Project Structure

```text
student-grade-tracker/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── settings.py
├── app/
│   ├── __init__.py
│   ├── wsgi.py
│   ├── routes/
│   ├── templates/
│   └── static/
├── student_grade_pkg/
│   ├── __init__.py
│   ├── database.py
│   ├── grade_manager.py
│   ├── student_manager.py
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_student_manager.py
│   └── test_grade_manager.py
└── docs/
    └── USAGE.md
```

## Contributing

1. Fork and create a feature branch.
2. Make focused, tested changes.
3. Run `pytest -q`.
4. Open a pull request with a clear description.

## License

This project is licensed under the MIT License.
