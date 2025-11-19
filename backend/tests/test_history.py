# tests/test_history.py
# 自动化测试：用户历史记录接口（增、查、删）

import json

def test_add_history(client):
    """测试添加历史记录接口"""
    payload = {
        "restaurant_name": "麦当劳",
        "timestamp": "2025-11-06T13:00:00"
    }
    response = client.post("/users/test001/history", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "History record added successfully"

def test_get_history(client):
    """测试获取用户历史记录接口"""
    response = client.get("/users/test001/history")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "restaurant_name" in data[0]
    assert "timestamp" in data[0]

def test_delete_history(client):
    """测试删除历史记录接口"""
    # 先获取一条记录
    get_response = client.get("/users/test001/history")
    data = get_response.get_json()
    if not data:
        assert False, "没有历史记录可删除"

    history_id = data[0]["id"]
    delete_response = client.delete(f"/history/{history_id}")
    assert delete_response.status_code == 200
    result = delete_response.get_json()
    assert result["message"] == "History record deleted successfully"
