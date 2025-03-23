# backend/posts/routes.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt

posts_bp = Blueprint('posts', __name__)
client = MongoClient("mongodb://localhost:27017")
db = client["postdb"]
collection = db["posts"]

SECRET_KEY = 'your-secret-key'

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"msg": "Missing or invalid token"}), 401
        try:
            token = token.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"msg": "Token is invalid or expired"}), 403
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

@posts_bp.route('/', methods=['GET'])
@token_required
def get_all_posts():
    posts = list(collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])
    return jsonify(posts), 200

@posts_bp.route('/<string:id>', methods=['GET'])
@token_required
def get_post(id):
    post = collection.find_one({"_id": ObjectId(id)})
    if post:
        post['_id'] = str(post['_id'])
        return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/', methods=['POST'])
@token_required
def create_post():
    data = request.get_json()
    post = {"title": data['title'], "body": data['body']}
    result = collection.insert_one(post)
    post['_id'] = str(result.inserted_id)
    return jsonify(post), 201

@posts_bp.route('/<string:id>', methods=['PUT'])
@token_required
def update_post(id):
    data = request.get_json()
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"title": data['title'], "body": data['body']}}
    )
    if result.matched_count:
        return jsonify({"msg": "Post updated"}), 200
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/<string:id>', methods=['DELETE'])
@token_required
def delete_post(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"msg": "Post deleted"}), 200
    return jsonify({"error": "Post not found"}), 404
