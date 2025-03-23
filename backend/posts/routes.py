from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

posts_bp = Blueprint('posts', __name__)

# Direct MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["postdb"]
collection = db["posts"]

@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    posts = list(collection.find())
    for post in posts:
        post['_id'] = str(post['_id'])
    return jsonify(posts), 200

@posts_bp.route('/<string:id>', methods=['GET'])
def get_post(id):
    post = collection.find_one({"_id": ObjectId(id)})
    if post:
        post['_id'] = str(post['_id'])
        return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/', methods=['POST'])
@posts_bp.route('', methods=['POST'])   
def create_post():
    data = request.get_json()
    post = {"title": data['title'], "body": data['body']}
    result = collection.insert_one(post)
    post['_id'] = str(result.inserted_id)
    return jsonify(post), 201

@posts_bp.route('/<string:id>', methods=['PUT'])
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
def delete_post(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"msg": "Post deleted"}), 200
    return jsonify({"error": "Post not found"}), 404
