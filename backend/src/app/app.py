
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

 # 从 .env 文件加载环境变量
from dotenv import load_dotenv



def create_app():
    load_dotenv() 

    app = Flask(__name__)
    CORS(app)

    init_extensions(app)
    
    # 注册蓝图
    #路由在这里做了统一注册，router里面分块编写
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(first_bp)
    app.register_blueprint(recommend_bp)

  
   #数据库初始化
   # （普通功能的路由定义请写在这之前
   
    with app.app_context():
         db.create_all()
   
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
