# test_history.py

import json
from datetime import datetime

def create_history(client, user_id, name, timestamp=None):
    payload = {"restaurant_name": name}
    if timestamp:
        payload["timestamp"] = timestamp
    return client.post(
        f"/api/users/{user_id}/history",
        data=json.dumps(payload),
        content_type="application/json"
    )


# =========================
# POST /api/users/<id>/history
# =========================

def test_create_history_success(client, db):
    res = create_history(
        client,
        "u001",
        "麦当劳",
        "2025-11-06T10:00:00Z"
    )

    assert res.status_code == 201
    assert res.json["data"]["restaurant_name"] == "麦当劳"
    assert res.json["data"]["user_id"] == "u001"


def test_create_missing_name(client):
    res = client.post(
        "/api/users/u001/history",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert res.status_code == 400


def test_create_without_timestamp(client):
    res = create_history(client, "u001", "海底捞")

    assert res.status_code == 201
    assert "timestamp" in res.json["data"]


# =============================
# GET /api/users/<id>/history
# =============================

def test_get_history_list(client, db):
    create_history(client, "u001", "A", "2025-11-06T11:00:00Z")
    create_history(client, "u001", "B", "2025-11-06T12:00:00Z")
    create_history(client, "u001", "C", "2025-11-06T10:00:00Z")

    res = client.get("/api/users/u001/history")

    assert res.status_code == 200

    data = res.json["data"]
    assert len(data) == 3

    assert data[0]["restaurant_name"] == "B"
    assert data[1]["restaurant_name"] == "A"
    assert data[2]["restaurant_name"] == "C"


def test_get_empty_history(client):
    res = client.get("/api/users/u002/history")
    assert res.status_code == 200
    assert res.json["data"] == []


def test_user_isolation(client, db):
    create_history(client, "u001", "麦当劳")
    create_history(client, "u002", "海底捞")

    res1 = client.get("/api/users/u001/history")
    res2 = client.get("/api/users/u002/history")

    assert len(res1.json["data"]) == 1
    assert len(res2.json["data"]) == 1


# =========================
# DELETE /api/history/<id>
# =========================

def test_delete_history_success(client, db):
    res = create_history(client, "u001", "麦当劳")
    history_id = res.json["data"]["id"]

    del_res = client.delete(f"/api/history/{history_id}")
    assert del_res.status_code == 200

    res2 = client.get("/api/users/u001/history")
    assert res2.json["data"] == []


def test_delete_not_found(client):
    res = client.delete("/api/history/99999")
    assert res.status_code == 404


def test_full_flow(client, db):
    h1 = create_history(client, "u001", "A")
    h2 = create_history(client, "u001", "B")

    id1 = h1.json["data"]["id"]
    id2 = h2.json["data"]["id"]

    res = client.get("/api/users/u001/history")
    assert len(res.json["data"]) == 2

    client.delete(f"/api/history/{id1}")

    res2 = client.get("/api/users/u001/history")
    assert len(res2.json["data"]) == 1
    assert res2.json["data"][0]["id"] == id2
