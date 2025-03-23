# backend/auth/routes.py
from flask import Blueprint, request, jsonify
import jwt
import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
client = MongoClient("mongodb://localhost:27017")
db = client["postdb"]
users_collection = db["users"]

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"msg": "User already exists"}), 409
    
    hashed_pw = generate_password_hash(data["password"])
    users_collection.insert_one({
        "email": data["email"],
        "password": hashed_pw
    })
    return jsonify({"msg": "Registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data["email"]})
    
    if user and check_password_hash(user["password"], data["password"]):
        token = jwt.encode({
            "user_id": str(user["_id"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, "your-secret-key", algorithm="HS256")
        
        return jsonify({"token": token}), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401
