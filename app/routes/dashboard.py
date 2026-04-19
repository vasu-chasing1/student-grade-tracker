"""Dashboard web and API routes."""

from __future__ import annotations

import sqlite3

from flask import Blueprint, current_app, jsonify, render_template


dashboard_bp = Blueprint("dashboard", __name__)


def _stats() -> dict:
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        total_grades = conn.execute("SELECT COUNT(*) FROM grades").fetchone()[0]
        avg_grade = conn.execute("SELECT AVG(grade_value) FROM grades").fetchone()[0]
        recent_grades = conn.execute(
            """
            SELECT student_id, subject, grade_value, semester
            FROM grades
            ORDER BY id DESC
            LIMIT 5
            """
        ).fetchall()

    return {
        "total_students": total_students,
        "total_grades": total_grades,
        "class_average": round(float(avg_grade), 2) if avg_grade is not None else 0.0,
        "recent_grades": [
            {
                "student_id": row[0],
                "subject": row[1],
                "grade_value": row[2],
                "semester": row[3],
            }
            for row in recent_grades
        ],
    }


@dashboard_bp.route("/")
def dashboard_page():
    return render_template("index.html", stats=_stats())


@dashboard_bp.route("/api/dashboard/stats", methods=["GET"])
def dashboard_stats():
    return jsonify(_stats()), 200
