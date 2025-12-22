# backend/src/app/app.py

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

from src.extensions import db, jwt, init_extensions

# 模型（确保能被 SQLAlchemy 扫描到）
from src.models import User
from src.models.history import History
from src.models.restaurant import Restaurant

# 蓝图
from src.routes.auth import auth_bp
from src.routes.home import home_bp
from src.routes.first import first_bp
from src.routes.history import history_bp
from src.routes.recommend import recommend_bp
from src.routes.restaurants import restaurants_bp
from src.routes.stats import stats_bp

from src.scheduler import start_scheduler


def create_app(testing=False):
    # 读取 .env
    load_dotenv()

    app = Flask(__name__)

    # ✅ 关键修改：精确 CORS 配置
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
    )

    # 数据库配置
    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化扩展（db / jwt）
    init_extensions(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(first_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(stats_bp)

    # 启动定时任务
    start_scheduler(app)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
