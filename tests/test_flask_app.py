"""Tests for Flask web and API interface."""

from __future__ import annotations

from flask.testing import FlaskClient


def test_dashboard_page_and_stats_api(app_client: FlaskClient) -> None:
    """Dashboard web and stats API should be available."""
    page = app_client.get("/")
    assert page.status_code == 200

    stats = app_client.get("/api/dashboard/stats")
    assert stats.status_code == 200
    assert stats.get_json()["total_students"] == 0


def test_students_api_crud(app_client: FlaskClient) -> None:
    """Students endpoints should support create/read/update/delete."""
    create_resp = app_client.post(
        "/api/students",
        json={"student_id": "S001", "name": "Raj Kumar"},
    )
    assert create_resp.status_code == 201

    list_resp = app_client.get("/api/students")
    assert list_resp.status_code == 200
    assert list_resp.get_json() == [{"student_id": "S001", "name": "Raj Kumar"}]

    read_resp = app_client.get("/api/students/S001")
    assert read_resp.status_code == 200

    update_resp = app_client.put("/api/students/S001", json={"name": "Raj K."})
    assert update_resp.status_code == 200
    assert update_resp.get_json()["name"] == "Raj K."

    delete_resp = app_client.delete("/api/students/S001")
    assert delete_resp.status_code == 204

    missing_resp = app_client.get("/api/students/S001")
    assert missing_resp.status_code == 404


def test_grades_api_and_filters(app_client: FlaskClient) -> None:
    """Grade endpoints should support create/list/by-student and filtering."""
    app_client.post("/api/students", json={"student_id": "S001", "name": "Raj Kumar"})
    app_client.post("/api/students", json={"student_id": "S002", "name": "Priya Singh"})

    create_grade = app_client.post(
        "/api/grades",
        json={
            "student_id": "S001",
            "subject": "Maths",
            "grade_type": "Test",
            "grade_value": 91,
            "semester": 1,
        },
    )
    assert create_grade.status_code == 201

    all_grades = app_client.get("/api/grades")
    assert all_grades.status_code == 200
    assert len(all_grades.get_json()) == 1

    by_student = app_client.get("/api/grades/S001")
    assert by_student.status_code == 200
    assert by_student.get_json()[0]["subject"] == "Maths"

    filtered = app_client.get("/api/grades", query_string={"subject": "math"})
    assert filtered.status_code == 200
    assert len(filtered.get_json()) == 1


def test_web_pages_and_validation(app_client: FlaskClient) -> None:
    """Students/grades pages should load and validate forms."""
    students_page = app_client.get("/students")
    assert students_page.status_code == 200

    bad_student_form = app_client.post("/students/add", data={"student_id": "", "name": ""})
    assert bad_student_form.status_code == 400

    app_client.post("/api/students", json={"student_id": "S010", "name": "Asha"})
    grades_page = app_client.get("/grades")
    assert grades_page.status_code == 200

    bad_grade_form = app_client.post(
        "/grades/add",
        data={"student_id": "S010", "subject": "", "grade_type": "Test", "grade_value": "99", "semester": "1"},
    )
    assert bad_grade_form.status_code == 400
