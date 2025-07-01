from typing import Dict
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from constants import Roles

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Uuid, primary_key=True, default=uuid4)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default=Roles.MEMBER, nullable=False)

    def __init__(self, email: str, password: str, role: str = Roles.MEMBER):
        self.id = uuid4()
        self.email = email
        self.role = role
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="bcrypt")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "email": self.email,
            "role": self.role,
        }
