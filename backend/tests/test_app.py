# tests/test_app.py
# 测试根路径 `/` 是否返回 200 且 message 正确，用于确认整个 Flask 应用正常启动
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.app.app import create_app  

def test_index_route():
    app = create_app()
    client = app.test_client()
    res = client.get('/')
    data = res.get_json()

    assert res.status_code == 200
    assert isinstance(data, dict)
    assert "message" in data
