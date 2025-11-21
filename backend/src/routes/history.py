# src/routes/history.py

from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.history import History
from datetime import datetime

history_bp = Blueprint('history', __name__)

# 1️⃣ 添加历史记录（POST /users/<user_id>/history）
@history_bp.route("/api/users/<string:user_id>/history", methods=["POST"])
def add_user_history(user_id):
    """
    新增浏览记录：
    1. 从请求体中取出 restaurant_name, timestamp
    2. 创建 History 记录并写入数据库
    3. 返回 201 状态码
    """
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


# 2️⃣ 查询某用户历史记录（GET /users/<user_id>/history）
@history_bp.route("/api/users/<string:user_id>/history", methods=["GET"])
def get_user_history(user_id):
    """
    查询用户浏览记录：
    - 按时间倒序返回所有记录
    """
    records = History.query.filter_by(user_id=user_id).order_by(History.timestamp.desc()).all()
    return jsonify([record.to_dict() for record in records]), 200


# 3️⃣ 删除某条历史记录（DELETE /history/<id>）
@history_bp.route("/history/<int:record_id>", methods=["DELETE"])
def delete_history(record_id):
    """
    删除浏览记录：
    - 找不到 → 返回 404
    - 成功删除 → 返回 200
    """
    #record = History.query.get(record_id)
    record = db.session.get(History, record_id)
    if not record:
        return jsonify({"message": "record not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "deleted"}), 200
