from flask import Blueprint, request, jsonify, Response
from typing import Any, Dict, List

from flask_jwt_extended import get_jwt_identity, jwt_required  # type: ignore
from models.user import db, User
from constants import HttpStatus, Roles
from uuid import UUID

user_bp: Blueprint = Blueprint("user_bp", __name__, url_prefix="/api/users")


@user_bp.route("", methods=["POST"])
@jwt_required()
def create_user() -> tuple[Response, int]:
    data: Dict[str, Any] = request.get_json(force=True)

    email: str | None = data.get("email")
    password: str | None = data.get("password")
    role: str | None = data.get("role")

    if not email or not password:
        return (
            jsonify({"message": "Email and password are required"}),
            HttpStatus.BAD_REQUEST,
        )

    if role not in Roles.ALL:
        return (
            jsonify({"message": f"Invalid role. Must be one of: {Roles.ALL}"}),
            HttpStatus.BAD_REQUEST,
        )

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), HttpStatus.CONFLICT

    new_user: User = User(email=email, password=password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify({"message": "User created successfully", "user": new_user.to_dict()}),
        201,
    )


@user_bp.route("", methods=["GET"])
@jwt_required()
def get_all_users() -> tuple[Response, int]:
    users: List[User] = db.session.query(User).all()
    user_list: list[Dict[str, str]] = [user.to_dict() for user in users]
    print(user_list)

    return jsonify({"users": user_list}), HttpStatus.OK


@user_bp.route("/<uuid:id>", methods=["GET"])
@jwt_required()
def get_user(id: UUID) -> tuple[Response, int]:
    user: User | None = db.session.query(User).get(id)
    print(user)

    if not user:
        return jsonify({"message": "User not found"}), HttpStatus.NOT_FOUND

    return jsonify({"user": user.to_dict()}), HttpStatus.OK


@user_bp.route("/<uuid:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id: UUID) -> tuple[Response, int]:
    user: User | None = db.session.query(User).get(id)
    print(id)

    if not user:
        return jsonify({"message": "User not found"}), HttpStatus.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), HttpStatus.OK


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_logged_in() -> tuple[Response, int]:
    user_id: UUID = get_jwt_identity()
    user: User | None = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "User not found"}), HttpStatus.NOT_FOUND

    return jsonify({"user": user.to_dict()}), HttpStatus.OK
