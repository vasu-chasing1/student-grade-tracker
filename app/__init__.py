"""Flask application factory."""

from __future__ import annotations

import os

from flask import Flask, jsonify
from flask_cors import CORS

from config.settings import get_settings
from student_grade_pkg.database import create_database


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask app."""
    settings = get_settings()
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(
        SECRET_KEY=os.getenv("SGT_SECRET_KEY", "dev-secret-key"),
        DB_PATH=settings.DB_PATH,
    )

    if test_config:
        app.config.update(test_config)

    create_database(app.config["DB_PATH"])
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes.dashboard import dashboard_bp
    from .routes.grades import grades_bp
    from .routes.students import students_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(grades_bp)

    @app.errorhandler(404)
    def not_found(_: Exception):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_: Exception):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(_: Exception):
        return jsonify({"error": "Internal server error"}), 500

    return app
