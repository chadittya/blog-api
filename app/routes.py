from flask import request, jsonify
from app import app
from app.models import User, Post
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from bson.errors import InvalidId

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    if User.find_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400
    User.create(username, password)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.find_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    result = Post.create(title, content, current_user)
    return jsonify({'message': 'Post created successfully', 'post_id': str(result.inserted_id)}), 201

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.get_all()
    return jsonify(posts), 200

@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.get_by_id(post_id)
        if post:
            return jsonify(post), 200
        else:
            return jsonify({'message': 'Post not found'}), 404
    except InvalidId:
        return jsonify({'message': 'Invalid post ID'}), 400

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Blog API"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Not Found"}), 404
