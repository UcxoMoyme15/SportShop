from flask import jsonify, g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager
from functools import wraps
from sqlalchemy.orm import relationship

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String(), default="Guest")


    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


def create_admin(User):
    admin = User.query.filter_by(role="Admin").first()
    if not admin:
        hashed_password = generate_password_hash("admin_password")
        admin = User(role="Admin", password=hashed_password)
        admin.create()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product(db.Model, BaseModel):

    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(), nullable=False)


current_user = {"username": "admin", "role": "admin"}


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user["role"] != "Admin":
            return jsonify()
        return f(*args, **kwargs)

    return decorated_function
