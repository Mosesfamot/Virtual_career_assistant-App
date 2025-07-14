from flask import Blueprint, request, jsonify
from db import users_collection
from models import hash_password, check_password
from flask_jwt_extended import create_access_token
import datetime

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200  # Preflight OK

    data = request.get_json()
    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 409

    user = {
        "username": data["username"],
        "email": data["email"],
        "password": hash_password(data["password"]),
        "createdAt": datetime.datetime.utcnow()
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

@auth.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200  # Preflight OK

    data = request.get_json()
    user = users_collection.find_one({"email": data["email"]})
    if not user or not check_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify(token=access_token), 200