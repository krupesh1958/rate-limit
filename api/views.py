"""This module constrainst all API."""
from flask import Blueprint, jsonify

bp = Blueprint("app", __name__)


@bp.route("/ask", methods=["GET"])
def post_questions() -> None:
    """
    Just simple testing API to check rate limit are workign properly or not.
    """
    return jsonify({
        "message": "Thank you for choosing me.",
        "data": None
    }, 200)
