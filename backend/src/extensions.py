#backend/src/extensions.py
# 初始Flack扩展实例

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from dotenv import load_dotenv
import os
import json

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def init_extensions(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "default_dev_key")

    db.init_app(app)
    jwt.init_app(app)

# JWT 错误处理
@jwt.invalid_token_loader
def invalid_token_loader(error_string):
    return jsonify({"code": 401, "message": "Token无效"}), 401

@jwt.unauthorized_loader
def unauthorized_loader(error_string):
    return jsonify({"code": 401, "message": "请先登录"}), 401

@jwt.expired_token_loader
def expired_token_loader(jwt_header, jwt_payload):
    return jsonify({"code": 401, "message": "登录已过期"}), 401

@jwt.revoked_token_loader
def revoked_token_loader(jwt_header, jwt_payload):
    return jsonify({"code": 401, "message": "Token已被撤销"}), 401