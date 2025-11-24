# backend/tests/test_auth.py
import json

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

def register(client, username, password):
    return client.post(
        "/api/auth/register",
        data=json.dumps({
            "username": username,
            "password": password
        }),
        content_type="application/json"
    )

def login(client, identifier, password):
    return client.post(
        "/api/auth/login",
        data=json.dumps({
            "identifier": identifier,
            "password": password
        }),
        content_type="application/json"
    )

# -------------------------------------------------
# Registration Tests
# -------------------------------------------------

def test_register_success(client, db):
    res = register(client, "alice", "123456")
    assert res.status_code == 201

    body = res.json
    assert body["code"] == 201
    assert body["message"] == "注册成功"
    assert "data" in body
    assert "user" in body["data"]
    assert body["data"]["user"]["username"] == "alice"
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


def test_register_missing_username(client):
    res = register(client, "", "123456")
    assert res.status_code == 400
    assert res.json["message"] == "用户名不能为空"


def test_register_missing_password(client):
    res = register(client, "bob", "")
    assert res.status_code == 400
    assert res.json["message"] == "密码不能为空"


def test_register_duplicate_username(client, db):
    register(client, "alice", "123456")
    res = register(client, "alice", "123456")

    assert res.status_code == 400
    assert res.json["message"] == "该用户名已存在，请重新输入"


# -------------------------------------------------
# Login Tests
# -------------------------------------------------

def test_login_success(client, db):
    reg = register(client, "alice", "123456")
    assert reg.status_code == 201

    res = login(client, "alice", "123456")
    assert res.status_code == 200
    body = res.json

    assert body["code"] == 200
    assert body["message"] == "登录成功"
    assert body["data"]["user"]["username"] == "alice"
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


def test_login_by_user_id(client, db):
    reg = register(client, "alice", "123456")
    user_id = reg.json["data"]["user"]["user_id"]

    res = login(client, user_id, "123456")
    assert res.status_code == 200

    body = res.json
    assert body["code"] == 200
    assert body["data"]["user"]["username"] == "alice"


def test_login_wrong_password(client, db):
    register(client, "alice", "123456")

    res = login(client, "alice", "wrongpass")
    assert res.status_code == 400
    assert res.json["message"] == "密码错误"


def test_login_user_not_found(client):
    res = login(client, "not_exist", "123123")
    assert res.status_code == 400
    assert res.json["message"] == "无效用户"


def test_login_missing_identifier(client):
    res = login(client, "", "123456")
    assert res.status_code == 400
    assert res.json["message"] == "请输入用户名或用户ID"


def test_login_missing_password(client):
    res = login(client, "alice", "")
    assert res.status_code == 400
    assert res.json["message"] == "请输入密码"


# -------------------------------------------------
# User Isolation
# -------------------------------------------------

def test_user_isolation(client, db):
    r1 = register(client, "alice", "123456")
    r2 = register(client, "bob", "654321")

    user_id_1 = r1.json["data"]["user"]["user_id"]
    user_id_2 = r2.json["data"]["user"]["user_id"]

    # 登录 alice
    res1 = login(client, user_id_1, "123456")
    assert res1.status_code == 200
    assert res1.json["data"]["user"]["username"] == "alice"

    # 登录 bob
    res2 = login(client, user_id_2, "654321")
    assert res2.status_code == 200
    assert res2.json["data"]["user"]["username"] == "bob"
