"""Grade web and API routes."""

from __future__ import annotations

import sqlite3

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for

from student_grade_pkg.grade_manager import GradeManager
from student_grade_pkg.student_manager import StudentManager

grades_bp = Blueprint("grades", __name__)


def _student_manager() -> StudentManager:
    return StudentManager(current_app.config["DB_PATH"])


def _grade_manager() -> GradeManager:
    return GradeManager(current_app.config["DB_PATH"])


def _query_grades(student_id_filter: str = "", subject_filter: str = "") -> list[dict]:
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute(
            """
            SELECT id, student_id, subject, grade_type, grade_value, semester
            FROM grades
            WHERE (? = '' OR student_id = ?)
              AND (? = '' OR LOWER(subject) LIKE ?)
            ORDER BY id DESC
            """,
            (
                student_id_filter,
                student_id_filter,
                subject_filter,
                f"%{subject_filter.lower()}%" if subject_filter else "",
            ),
        )
        return [
            {
                "id": row[0],
                "student_id": row[1],
                "subject": row[2],
                "grade_type": row[3],
                "grade_value": row[4],
                "semester": row[5],
            }
            for row in cursor.fetchall()
        ]


@grades_bp.route("/grades")
def list_grades_page():
    student_id = request.args.get("student_id", "").strip()
    subject = request.args.get("subject", "").strip()
    grades = _query_grades(student_id, subject)
    students = _student_manager().get_all_students()
    return render_template(
        "grades/list.html",
        grades=grades,
        students=students,
        student_id=student_id,
        subject=subject,
    )


@grades_bp.route("/grades/add", methods=["GET", "POST"])
def add_grade_page():
    student_mgr = _student_manager()
    students = student_mgr.get_all_students()

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        subject = request.form.get("subject", "").strip()
        grade_type = request.form.get("grade_type", "").strip()
        grade_value_raw = request.form.get("grade_value", "").strip()
        semester_raw = request.form.get("semester", "").strip()

        if not all([student_id, subject, grade_type, grade_value_raw, semester_raw]):
            flash("All fields are required.", "danger")
            return render_template("grades/add.html", students=students), 400

        try:
            grade_value = int(grade_value_raw)
            semester = int(semester_raw)
        except ValueError:
            flash("Grade value and semester must be numbers.", "danger")
            return render_template("grades/add.html", students=students), 400

        if not _grade_manager().add_grade(student_id, subject, grade_type, grade_value, semester):
            flash("Unable to add grade. Check student and values.", "danger")
            return render_template("grades/add.html", students=students), 400

        flash("Grade added successfully.", "success")
        return redirect(url_for("grades.list_grades_page"))

    return render_template("grades/add.html", students=students)


@grades_bp.route("/api/grades", methods=["GET", "POST"])
def grades_collection():
    if request.method == "GET":
        student_id = request.args.get("student_id", "").strip()
        subject = request.args.get("subject", "").strip()
        return jsonify(_query_grades(student_id, subject)), 200

    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    subject = str(data.get("subject", "")).strip()
    grade_type = str(data.get("grade_type", "")).strip()

    try:
        grade_value = int(data.get("grade_value"))
        semester = int(data.get("semester"))
    except (TypeError, ValueError):
        return jsonify({"error": "grade_value and semester must be integers"}), 400

    if not student_id or not subject or not grade_type:
        return jsonify({"error": "student_id, subject, and grade_type are required"}), 400
    if not _student_manager().get_student(student_id):
        return jsonify({"error": "student not found"}), 404
    if not _grade_manager().add_grade(student_id, subject, grade_type, grade_value, semester):
        return jsonify({"error": "unable to create grade"}), 400

    return (
        jsonify(
            {
                "student_id": student_id,
                "subject": subject,
                "grade_type": grade_type,
                "grade_value": grade_value,
                "semester": semester,
            }
        ),
        201,
    )


@grades_bp.route("/api/grades/<student_id>", methods=["GET"])
def student_grades(student_id: str):
    if not _student_manager().get_student(student_id):
        return jsonify({"error": "student not found"}), 404

    grades = _grade_manager().get_student_grades(student_id)
    payload = [
        {
            "subject": subject,
            "grade_type": grade_type,
            "grade_value": grade_value,
            "semester": semester,
        }
        for subject, grade_type, grade_value, semester in grades
    ]
    return jsonify(payload), 200
