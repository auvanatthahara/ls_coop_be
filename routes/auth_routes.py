from typing import Any, Dict
from uuid import UUID
from flask import Blueprint, Response, current_app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required  # type: ignore

from constants import HttpStatus
from models.user import db, User

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
    data: Dict[str, Any] = request.get_json()
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    if not email or not password:
        return (
            jsonify({"message": "Email and password required"}),
            HttpStatus.BAD_REQUEST,
        )

    user = db.session.query(User).filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), HttpStatus.UNAUTHORIZED

    access_token: str = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), HttpStatus.OK


@auth_bp.route("/change-password/<uuid:id>", methods=["PUT"])
@jwt_required()
def change_password(id: UUID) -> tuple[Response, int]:
    data: Dict[str, Any] = request.get_json(force=True)

    old_password: str | None = data.get("old_password")
    new_password: str | None = data.get("new_password")
    user: User | None = db.session.query(User).get(id)

    if not new_password:
        return jsonify({"message": "New password is required"}), HttpStatus.BAD_REQUEST

    if not old_password:
        return jsonify({"message": "Old password is required"}), HttpStatus.BAD_REQUEST

    if not user:
        return jsonify({"message": "User not found"}), HttpStatus.NOT_FOUND

    if user.check_password(old_password):
        return (
            jsonify({"message": "Old password is incorrect"}),
            HttpStatus.UNAUTHORIZED,
        )

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), HttpStatus.OK


@auth_bp.route("/dev-token", methods=["GET"])
def dev_token():
    if current_app.config.get("APP_ENV") != "development":  # type: ignore
        return jsonify({"message": "Unauthorized"}), HttpStatus.UNAUTHORIZED

    fake_user_id = "00000000-0000-0000-0000-000000000000"
    token = create_access_token(identity=fake_user_id)
    return jsonify({"token": token})
