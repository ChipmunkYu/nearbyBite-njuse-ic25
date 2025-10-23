
from flask import Flask, jsonify


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

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
