# backend/src/routes/auth.py
from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.user import User, generate_account_number
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

# ====== 导入爬虫（新增）======
from crawler.sources.crawler_simple import run_crawler_main

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def make_unique_user_id(k=8):
    for _ in range(100):
        candidate = generate_account_number(k)
        if not User.query.filter_by(user_id=candidate).first():
            return candidate

    import time
    return f"{User.generate_user_id(k - 3)}{int(time.time()) % 10000}"


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username:
        return jsonify({"code": 400, "message": "用户名不能为空"}), 400
    if not password:
        return jsonify({"code": 400, "message": "密码不能为空"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "message": "该用户名已存在，请重新输入"}), 400

    # 生成唯一的用户ID
    user_id = make_unique_user_id(k=8)

    user = User(username=username, user_id=user_id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=4))
    refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=7))

    return jsonify({
        "code": 201,
        "message": "注册成功",
        "data": {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = (data.get("identifier") or "").strip()
    password = (data.get("password") or "").strip()

    if not identifier:
        return jsonify({"code": 400, "message": "请输入用户名或用户ID"}), 400
    if not password:
        return jsonify({"code": 400, "message": "请输入密码"}), 400

    # 先查 username，再查 user_id
    user = User.query.filter_by(username=identifier).first()

    if not user:
        user = User.query.filter_by(user_id=identifier).first()
        if not user:
            return jsonify({"code": 400, "message": "无效用户"}), 400

    if not user.check_password(password):
        return jsonify({"code": 400, "message": "密码错误"}), 400

    # 登录成功后自动执行爬虫 
    try:
        print("[登录触发爬虫] 正在更新餐馆数据库...")
        run_crawler_main()
        print("[登录触发爬虫] 数据更新完成")
    except Exception as e:
        # 错误不影响登录流程
        print("[登录触发爬虫] 更新失败:", e)

    # 生成 JWT
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=4))
    refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=7))

    return jsonify({
        "code": 200,
        "message": "登录成功",
        "data": {
            "access_token": token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }
    }), 200


# 临时测试接口
@auth_bp.route("/test/add-user", methods=["POST"])
def add_fake_user():
    user = User(
        user_id="test001",
        username="testuser"
    )
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Test user added", "user_id": user.id}), 201
