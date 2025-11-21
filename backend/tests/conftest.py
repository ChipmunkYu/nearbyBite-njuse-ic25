# backend/tests/conftest.py
import sys
import os
import pytest

# ✅ 关键：添加 backend 的上一级目录（项目根目录）
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
print("✔ 已将路径加入 sys.path:", ROOT_DIR)

from src.app.app import create_app  # ✅ 注意这里的路径改为 backend.src.app

@pytest.fixture
def client():
    """创建 Flask 测试客户端"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
