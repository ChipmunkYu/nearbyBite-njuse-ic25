
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.extensions import db, jwt, init_extensions
#新表添加后请import（可以直接写在User后面或者另起一行重import）
from src.models import User
from src.routes.auth import auth_bp
import os

 # 从 .env 文件加载环境变量
from dotenv import load_dotenv

def create_app():
    load_dotenv() 

    app = Flask(__name__)
    CORS(app)

    init_extensions(app)
  
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return {'message': 'Hello from Flask backend!'}

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

   
   
   #数据库初始化
   # （普通功能的路由定义请写在这之前
   # 想要分块一点写在routes文件夹，参考auth）
   
    with app.app_context():
         db.create_all()
   
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
