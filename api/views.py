"""This module constrainst all API."""
from flask import Blueprint, jsonify

bp = Blueprint("app", __name__)


@bp.route("/ask", methods=["GET"])
def post_questions() -> None:
    """
    Simple API for testing the rate limit algorithms.
    """
    return jsonify({
        "message": "Thank you for choosing me.",
        "data": None
    }), 200
