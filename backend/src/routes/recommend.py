#这里是推荐餐厅的接口，占一个大致的位，做recommend的同学根据情况进行修改
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

#访问路径：http://127.0.0.1:5000/api/recommend/restaurants


recommend_bp = Blueprint("recommend", __name__, url_prefix="/api/recommend")

@recommend_bp.route("/restaurants", methods=["GET"])

#表示需要身份验证才能访问此路由，根据具体实际情况决定是否需要添加,这里相关的同学可以不用管，只用写业务逻辑就行（可以直接删除）
#@jwt_required()

def recommend():
        # 如果用了 @jwt_required() 最好使用这个
        #user_id = get_jwt_identity() 
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
