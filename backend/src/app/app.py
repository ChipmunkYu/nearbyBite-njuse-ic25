# backend/src/app/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.extensions import  db, jwt, init_extensions
#新表添加后请import（可以直接写在User后面或者另起一行重import）
from src.models import User
from src.routes.auth import auth_bp
from src.routes.home import home_bp
from src.routes.first import first_bp
from src.routes.history import history_bp  # 新增
from src.routes.recommend import recommend_bp
from src.routes.restaurants import restaurants_bp
from src.routes.stats import stats_bp
# 模型：新增 History 表（用于历史记录）
from src.models.history import History  # 加入历史模型（不写也能建表，但最好显式 import 让 IDE 检查语法）
from src.models.restaurant import Restaurant  # 加入餐厅模型
# 路由蓝图：引入历史记录接口
from src.routes.users import users_bp  # 用户相关接口


import os
from dotenv import load_dotenv

def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # 测试环境：使用内存数据库
    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # 初始化扩展 (db, jwt 等)
    init_extensions(app)

    # 注册路由
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp) 
    app.register_blueprint(home_bp)
    app.register_blueprint(first_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(stats_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)