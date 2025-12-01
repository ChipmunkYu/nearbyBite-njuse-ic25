from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone

from src.models.user import User
from src.models.history import History
from src.extensions import db

first_bp = Blueprint("first", __name__, url_prefix="/api/first")

@first_bp.route('/info', methods=['GET'])
@jwt_required()
def first_info():
    uid = get_jwt_identity()

    user = User.query.get(uid)
    if not user:
        return jsonify({"code":404, "message":"用户不存在"}), 404

    # 统计推荐次数（历史记录数量）
    total_recommend = (
        db.session.query(History)
        .filter(History.user_id == uid)
        .count()
    )

    # 统计本周推荐次数（过去七天）
    today = datetime.now(timezone.utc).date()
    week_start = today - timedelta(days=6)

    week_recommend = (
        db.session.query(History)
        .filter(History.user_id == uid,
                History.timestamp >= week_start)
        .count()
    )

    # 使用天数
    if user.created_at:
        days_used = (today - user.created_at.date()).days + 1
    else:
        days_used = 1

    return jsonify({
        "code": 200,
        "message": "First page(need to login)",
        "data": {
            "user": {
                "id": user.id,
                "username": user.username
            },
            "tips": "This is some protected information only for logged-in users.",
            "stats": {
                "total_recommend": total_recommend,
                "week_recommend": week_recommend,
                "days_used": days_used
            }
        }
    })
