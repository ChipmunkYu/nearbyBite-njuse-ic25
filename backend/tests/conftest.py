# backend/tests/conftest.py
import sys
import os
import pytest

# ✅ 关键：添加 backend 的上一级目录（项目根目录）
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
print("✔ 已将路径加入 sys.path:", ROOT_DIR)

from src.app.app import create_app 
from src.extensions import db as _db

@pytest.fixture
def app():
    """创建 Flask 测试 app（使用测试配置）"""
    app = create_app(testing=True)  # 要支持 testing=True
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # 内存数据库方便测试

    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    """为测试创建空数据库"""
    _db.drop_all()
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture
def client(app, db):
    """Flask 测试客户端"""
    return app.test_client()