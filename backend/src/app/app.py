
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

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

    # Registion interface (fake data now)
    @app.route("/auth/register", methods=["POST"])
    def register():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")        
    # 后续丰富判断逻辑
        if not username :
            return jsonify({"error": "用户名不能为空"}), 400
        if not password :
            return jsonify({"error": "密码不能为空"}), 400
        
        return jsonify({"message": "注册成功",
                        "user" : {"username" : username}
                        }), 201

    # Login interface (fake data now)
    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        # 后续丰富判断逻辑
        if username == "testuser" and password == "testpass":
            return jsonify({"message": "登录成功",
                            "token" : "fake-jwt-token"
                            }), 200
        else:
            return jsonify({"error": "无效的用户名或密码"}), 401


    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
