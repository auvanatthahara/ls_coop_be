# routes/user_routes.py

from flask import Blueprint, request, jsonify, Response
from typing import Any, Dict
from models.user import db, User
from constants import Roles

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/users")


@user_bp.route("", methods=["POST"])
def create_user() -> tuple[Response, int]:
    data: Dict[str, Any] = request.get_json(force=True)

    email: str | None = data.get("email")
    password: str | None = data.get("password")
    role: str | None = data.get("role")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if role not in Roles.ALL:
        return jsonify({"message": f"Invalid role. Must be one of: {Roles.ALL}"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    new_user = User(email=email, password=password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify({"message": "User created successfully", "user": new_user.to_dict()}),
        201,
    )
