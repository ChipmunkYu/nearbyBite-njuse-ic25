from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extensions import db
from src.models.user import User
import traceback

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# -------------------------------
# 获取当前用户信息
# -------------------------------
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"code": 404, "message": "用户不存在"}), 404

        return jsonify({
            "code": 200,
            "message": "获取成功",
            "data": user.to_dict()
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"code": 500, "message": f"获取用户信息失败: {str(e)}"}), 500


# -------------------------------
# 修改用户名
# -------------------------------
@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_username():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"code": 404, "message": "用户不存在"}), 404

        data = request.get_json() or {}
        new_username = (data.get("username") or "").strip()

        if not new_username:
            return jsonify({"code": 400, "message": "用户名不能为空"}), 400

        # 检查是否重名
        exists = User.query.filter(
            User.username == new_username,
            User.id != user_id
        ).first()

        if exists:
            return jsonify({"code": 400, "message": "该用户名已被使用"}), 400

        user.username = new_username
        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "用户名修改成功",
            "data": user.to_dict()
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"code": 500, "message": f"修改失败: {str(e)}"}), 500


# -------------------------------
# 修改密码
# -------------------------------
@users_bp.route("/me/password", methods=["POST"])
@jwt_required()
def change_password():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"code": 404, "message": "用户不存在"}), 404

        data = request.get_json() or {}
        old_pwd = (data.get("oldPwd") or "").strip()
        new_pwd = (data.get("newPwd") or "").strip()

        if not old_pwd or not new_pwd:
            return jsonify({"code": 400, "message": "密码不能为空"}), 400

        if not user.check_password(old_pwd):
            return jsonify({"code": 400, "message": "旧密码错误"}), 400

        user.set_password(new_pwd)
        db.session.commit()

        return jsonify({"code": 200, "message": "密码修改成功"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"code": 500, "message": f"修改失败: {str(e)}"}), 500
