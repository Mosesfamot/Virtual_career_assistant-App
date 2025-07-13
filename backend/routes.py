from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import responses_collection, users_collection
from bson import ObjectId
import datetime

routes = Blueprint("routes", __name__)

@routes.route("/submit-response", methods=["POST"])
@jwt_required()
def submit_response():
    data = request.get_json()
    user_id = get_jwt_identity()

    print("Data received:", data)  # Debug
    if "prompt" not in data or "response" not in data:
        return jsonify({"error": "Missing prompt or response in request body"}), 400

    responses_collection.insert_one({
        "userId": ObjectId(user_id),
        "prompt": data["prompt"],
        "response": data["response"],
        "createdAt": datetime.datetime.utcnow()
    })
    return jsonify({"message": "Response saved successfully"}), 201

@routes.route("/my-responses", methods=["GET"])
@jwt_required()
def get_my_responses():
    user_id = get_jwt_identity()
    results = list(responses_collection.find({"userId": ObjectId(user_id)}))

    for res in results:
        res["_id"] = str(res["_id"])
        res["userId"] = str(res["userId"])
        if "createdAt" in res and hasattr(res["createdAt"], "isoformat"):
            res["createdAt"] = res["createdAt"].isoformat()
    return jsonify(results)

@routes.route("/all-responses", methods=["GET"])
@jwt_required()
def get_all_responses():
    try:
        user_id = get_jwt_identity()
        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user or user.get("role") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        results = list(responses_collection.find())
        for res in results:
            res["_id"] = str(res["_id"])
            if "userId" in res:
                res["userId"] = str(res["userId"])
            if "createdAt" in res and hasattr(res["createdAt"], "isoformat"):
                res["createdAt"] = res["createdAt"].isoformat()

        print("Admin user accessing /all-responses")
        print("Results count:", len(results))
        return jsonify(results)

    except Exception as e:
        print("Error in /all-responses:", str(e))
        return jsonify({"error": "Internal server error"}), 500
