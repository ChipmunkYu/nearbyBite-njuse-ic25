from flask import Flask, jsonify, request
from flask_cors import CORS
from src.extensions import db, jwt, init_extensions
#新表添加后请import（可以直接写在User后面或者另起一行重import）
from src.models import User
from src.routes.auth import auth_bp
from src.routes.home import home_bp
from src.routes.first import first_bp
from src.routes.recommend import recommend_bp
import os


# 模型：新增 History 表（用于历史记录）
from src.models.history import History  # 加入历史模型（不写也能建表，但最好显式 import 让 IDE 检查语法）

# 路由蓝图：引入历史记录接口

from src.routes.history import history_bp  # 新增

import os
from dotenv import load_dotenv



def create_app():
    load_dotenv()  # 读取 .env 环境变量

    app = Flask(__name__)
    CORS(app)  # 允许跨域

    init_extensions(app)
    
    # 注册蓝图
    #路由在这里做了统一注册，router里面分块编写
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(first_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(history_bp)  # 注册历史记录蓝图
  
   #数据库初始化
   # （普通功能的路由定义请写在这之前
   
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
