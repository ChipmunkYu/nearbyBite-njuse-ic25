from flask import Blueprint, request, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def index():
    return jsonify({'message': 'Hello from Flask backend!'})
