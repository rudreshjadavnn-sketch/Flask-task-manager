from flask import Blueprint, request, jsonify
from database import users_collection
from config import Config
import bcrypt
import jwt
import datetime
from utils.validators import valid_email, valid_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not valid_email(email):
        return jsonify({
            "message": "Invalid Email"
        }), 400

    if not valid_password(password):
        return jsonify({
            "message": "Password must contain minimum 8 characters"
        }), 400

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 409

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({
        "message": "Registration Successful"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and Password required"
        }), 400

    user = users_collection.find_one({
        "email": email
    })

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"]
    ):
        return jsonify({
            "message": "Wrong Password"
        }), 401

    token = jwt.encode(
        {
            "email": email,
            "name": user["name"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "name": user["name"],
        "email": email
    }), 200