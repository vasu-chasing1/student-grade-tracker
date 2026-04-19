"""Student web and API routes."""

from __future__ import annotations

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for

from student_grade_pkg.student_manager import StudentManager

students_bp = Blueprint("students", __name__)


def _student_manager() -> StudentManager:
    return StudentManager(current_app.config["DB_PATH"])


@students_bp.route("/students")
def list_students_page():
    query = request.args.get("q", "").strip().lower()
    students = _student_manager().get_all_students()
    if query:
        students = [row for row in students if query in row[0].lower() or query in row[1].lower()]
    return render_template("students/list.html", students=students, query=query)


@students_bp.route("/students/add", methods=["GET", "POST"])
def add_student_page():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        name = request.form.get("name", "").strip()
        if not student_id or not name:
            flash("Student ID and name are required.", "danger")
            return render_template("students/add.html", student_id=student_id, name=name), 400
        if _student_manager().add_student(student_id, name):
            flash("Student added successfully.", "success")
            return redirect(url_for("students.list_students_page"))
        flash("Unable to add student. ID may already exist.", "danger")
        return render_template("students/add.html", student_id=student_id, name=name), 400
    return render_template("students/add.html")


@students_bp.route("/students/<student_id>/delete", methods=["POST"])
def delete_student_page(student_id: str):
    if _student_manager().delete_student(student_id):
        flash("Student deleted successfully.", "success")
    else:
        flash("Student not found.", "warning")
    return redirect(url_for("students.list_students_page"))


@students_bp.route("/api/students", methods=["GET", "POST"])
def students_collection():
    manager = _student_manager()
    if request.method == "GET":
        query = request.args.get("q", "").strip().lower()
        students = manager.get_all_students()
        if query:
            students = [row for row in students if query in row[0].lower() or query in row[1].lower()]
        payload = [{"student_id": student_id, "name": name} for student_id, name in students]
        return jsonify(payload), 200

    data = request.get_json(silent=True) or {}
    student_id = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()

    if not student_id or not name:
        return jsonify({"error": "student_id and name are required"}), 400
    if manager.get_student(student_id):
        return jsonify({"error": "student already exists"}), 409
    if not manager.add_student(student_id, name):
        return jsonify({"error": "unable to create student"}), 400

    return jsonify({"student_id": student_id, "name": name}), 201


@students_bp.route("/api/students/<student_id>", methods=["GET", "PUT", "DELETE"])
def student_item(student_id: str):
    manager = _student_manager()
    student = manager.get_student(student_id)

    if request.method == "GET":
        if not student:
            return jsonify({"error": "student not found"}), 404
        return jsonify({"student_id": student[0], "name": student[1]}), 200

    if request.method == "PUT":
        if not student:
            return jsonify({"error": "student not found"}), 404
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()
        if not name:
            return jsonify({"error": "name is required"}), 400
        if not manager.update_student(student_id, name):
            return jsonify({"error": "unable to update student"}), 400
        return jsonify({"student_id": student_id, "name": name}), 200

    if not student:
        return jsonify({"error": "student not found"}), 404
    manager.delete_student(student_id)
    return "", 204
