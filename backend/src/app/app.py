from flask import Flask, jsonify, request
from flask_cors import CORS
from ..extensions import db, jwt, init_extensions


# 模型：新增 History 表（用于历史记录）
from ..models import User   # 已有用户模型
from ..models.user import User
from ..models.history import History  # 加入历史模型（不写也能建表，但最好显式 import 让 IDE 检查语法）

# 路由蓝图：引入历史记录接口
from ..routes.auth import auth_bp
from ..routes.history import history_bp  # 新增

import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()  # 读取 .env 环境变量

    app = Flask(__name__)
    CORS(app)  # 允许跨域

    init_extensions(app)  # 初始化 db、jwt 等扩展

    # 注册接口蓝图（路由拆分写在 routes 文件夹）
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)  # 新增：注册 history 模块路由

    # 默认主页路由（测试用）
    @app.route('/')
    def index():
        return {'message': 'Hello from Flask backend!'}

    # 示例推荐接口（测试用，未来 B 模块成员会替换）
    @app.route("/restaurants/recommend", methods=["GET"])
    def recommend():
        return jsonify([
            {
                "name": "麦当劳",
                "location": "中山路",
                "tags": ["快餐", "人均30"]
            },
            {
                "name": "肯德基",
                "location": "南大门口",
                "tags": ["鸡肉", "人均35"]
            }
        ])

    # 自动建表（只在首次创建数据库时有用）
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
