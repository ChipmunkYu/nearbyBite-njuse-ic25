# 功能：提供用户浏览记录的查询、添加和删除接口

from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.history import History
from datetime import datetime

# ✅ url_prefix 为空，方便直接定义完整路径
history_bp = Blueprint("history", __name__, url_prefix="")

# 1️⃣ 添加历史记录（POST /users/<user_id>/history）
@history_bp.route("/users/<string:user_id>/history", methods=["POST"])
def add_user_history(user_id):
    """
    新增浏览记录：
    1. 从请求体中取出 restaurant_name, timestamp
    2. 创建 History 记录并写入数据库
    3. 返回 201 状态码
    """
    data = request.get_json()
    restaurant_name = data.get("restaurant_name")
    timestamp_str = data.get("timestamp")
    timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()

    record = History(user_id=user_id, restaurant_name=restaurant_name, timestamp=timestamp)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "History record added successfully"}), 201


# 2️⃣ 查询某用户历史记录（GET /users/<user_id>/history）
@history_bp.route("/users/<string:user_id>/history", methods=["GET"])
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
    record = History.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "History record deleted successfully"}), 200

