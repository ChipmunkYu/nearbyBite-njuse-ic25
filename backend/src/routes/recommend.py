from flask import Blueprint, request, jsonify
import random

from src.utils.recommend_query import build_restaurant_query
from src.models.restaurant import Restaurant

recommend_bp = Blueprint("recommend", __name__, url_prefix="/api/recommend")


@recommend_bp.route("/restaurants", methods=["GET"])
def recommend():

    # 读取参数
    filters = {
        "price_min": request.args.get("price_min", 0, type=float),
        "price_max": request.args.get("price_max", 9999, type=float),
        "min_rating": request.args.get("min_rating", None, type=float),
        "area": request.args.get("area", "", type=str),
        "types": [t for t in request.args.get("types", "").split(",") if t],
        "flavors": [f for f in request.args.get("flavors", "").split(",") if f],
    }

    # 构建查询
    query = build_restaurant_query(filters)

    # 限制候选数量
    candidates = query.limit(100).all()

    # 无结果
    if not candidates:
        return jsonify({
            "code": 200,
            "message": "no match",
            "count": 0,
            "data": []
        }), 200

    # 随机抽一条
    chosen = random.choice(candidates)

    return jsonify({
        "code": 200,
        "message": "success",
        "count": 1,
        "data": [chosen.to_dict()]
    }), 200