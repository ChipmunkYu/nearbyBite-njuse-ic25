from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.history import History
from datetime import datetime, timezone
from flask_jwt_extended import jwt_required, get_jwt_identity
def utc_now():
    return datetime.now(timezone.utc)

history_bp = Blueprint('history', __name__)


#  1) 创建历史记录

@history_bp.route('/api/users/me/history', methods=['POST'])
@jwt_required()
def create_history():
    uid = get_jwt_identity()
    data = request.get_json()
    restaurant_name = data.get("restaurant_name")
    restaurant_id = data.get("restaurant_id")
    timestamp = data.get("timestamp")  # ISO8601 字符串

    if not restaurant_name:
        return jsonify({"message": "restaurant_name is required"}), 400

    if timestamp:
        timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    else:
        timestamp =datetime.now(timezone.utc)

    record = History(
        user_id=uid,
        restaurant_name=restaurant_name,
         restaurant_id=restaurant_id,
        timestamp=timestamp
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "History record added successfully", "data": record.to_dict()}), 201


#  2) 获取用户所有历史记录

@history_bp.route('/api/users/me/history', methods=['GET'])
@jwt_required()
def get_history():
    uid = get_jwt_identity()
    records = History.query.filter_by(user_id=uid).order_by(History.timestamp.desc()).all()
    return jsonify({"data": [r.to_dict() for r in records]}), 200



#  3) 删除历史记录

@history_bp.route('/api/users/me/history/<history_id>', methods=['DELETE'])
@jwt_required()
def delete_history(history_id):
    uid = int(get_jwt_identity())
    #record = History.query.get(history_id)
    record = db.session.get(History, history_id)
    print("DEBUG DELETE:", "uid=", uid, "record_user_id=", record.user_id)

    if not record:
        return jsonify({"message": "record not found"}), 404

    if record.user_id != uid:
        return jsonify({"message": "permission denied"}), 403
   
    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "History record deleted successfully"}), 200
