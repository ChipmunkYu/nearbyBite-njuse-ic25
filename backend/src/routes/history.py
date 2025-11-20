# src/routes/history.py

from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.history import History
from datetime import datetime

history_bp = Blueprint('history', __name__)

##########################################
#  1) 创建历史记录
##########################################
@history_bp.route('/users/<user_id>/history', methods=['POST'])
def create_history(user_id):
    data = request.get_json()
    restaurant_name = data.get("restaurant_name")
    timestamp = data.get("timestamp")  # ISO8601 字符串

    if not restaurant_name:
        return jsonify({"message": "restaurant_name is required"}), 400

    # timestamp 解析（如果前端传 ISO8601）
    if timestamp:
        timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    else:
        timestamp = datetime.utcnow()

    record = History(
        user_id=user_id,
        restaurant_name=restaurant_name,
        timestamp=timestamp
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "data": record.to_dict()}), 201


##########################################
#  2) 获取用户所有历史记录

@history_bp.route('/users/<user_id>/history', methods=['GET'])
def get_history(user_id):
    records = History.query.filter_by(user_id=user_id)\
                .order_by(History.timestamp.desc()).all()
    return jsonify({
        "data": [r.to_dict() for r in records]
    }), 200


##########################################
#  3) 删除历史记录

@history_bp.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    record = History.query.get(history_id)

    if not record:
        return jsonify({"message": "record not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "deleted"}), 200
