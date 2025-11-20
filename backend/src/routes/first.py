from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# http://127.0.0.1:5000/api/first/info

first_bp = Blueprint("first", __name__, url_prefix="/api/first")

@first_bp.route('/info', methods=['GET'])
@jwt_required()

def first_info():
    user_id = get_jwt_identity()
    return jsonify({
        "code": 200,
        'message': 'Fierst page(need to login)',
        'data': {
            'user': user_id,
            "tips": "This is some protected information only for logged-in users."
        }
        })
