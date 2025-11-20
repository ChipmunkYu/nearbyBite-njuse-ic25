from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta

refresh_bp = Blueprint("refresh", __name__, url_prefix="/api")

@refresh_bp.route("/refresh", methods=["POST"])

@jwt_required(refresh=True)  
def refresh():
    identity = get_jwt_identity()
    new_access = create_access_token(identity=identity, expires_delta=timedelta(hours=2))
    return jsonify({
        "code": 200,
        "message": "Token刷新成功",
        "data": {
            "access_token": new_access
        }
    })