# src/app/recommend.py
import random
from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models.restaurant import Restaurant
from src.utils.recommend_query import (
    plane_distance,
    sample_restaurants
)
from flask_jwt_extended import jwt_required

recommend_bp = Blueprint("recommend", __name__, url_prefix="/api/recommend")

_LAST_IDS = []
_LAST_CAP = 10


@recommend_bp.route("/restaurants", methods=["GET"])
@jwt_required()
def recommend():

    # === 参数 ===
    price_min = request.args.get("price_min", 0, type=float)
    price_max = request.args.get("price_max", 9999, type=float)
    min_rating = request.args.get("min_rating", None, type=float)
    area = request.args.get("area", "", type=str)

    types = [t for t in request.args.get("types", "", type=str).split(",") if t]
    flavors = [f for f in request.args.get("flavors", "", type=str).split(",") if f]

    # 距离筛选参数
    max_distance = request.args.get("max_distance_km", None, type=float)
    user_lat = request.args.get("lat", None, type=float)
    user_lng = request.args.get("lng", None, type=float)

    # === 查询数据库 ===
    query = Restaurant.query

    # 价格区间
    query = query.filter(
        Restaurant.avg_price >= price_min,
        Restaurant.avg_price <= price_max
    )

    # 评分
    if min_rating is not None:
        query = query.filter(Restaurant.rating >= min_rating)

    # 地区（address中包含 area 字段）
    if area and area not in ["全部", "all", "undefined", "null"]:
        query = query.filter(Restaurant.address.like(f"%{area}%"))

    candidates = query.all()

    # === 转换为你同学的格式（兼容前端） ===
    candidates_list = [
        {
            "id": r.id,
            "name": r.name,
            "location": r.address,
            "area": r.address,
            "price": r.avg_price or 0,
            "rating": r.rating or 0,
            "types": r.tags or [],
         #  "flavors": [],  # 你数据库没有 flavors 字段
            "lat": r.latitude or 0,
            "lng": r.longitude or 0
        }
        for r in candidates
    ]

    # === 处理类型过滤 ===
    if types:
        candidates_list = [
            r for r in candidates_list
            if any(t in (r["types"] or []) for t in types)
        ]

    # === 处理口味 filters（你的 DB 没有，这里保持兼容空）===
    if flavors:
        candidates_list = [
            r for r in candidates_list
            if any(f in (r["flavors"] or []) for f in flavors)
        ]

    # === 距离过滤 ===
    if user_lat and user_lng and max_distance:
        candidates_list = [
            r for r in candidates_list
            if plane_distance(user_lat, user_lng, r["lat"], r["lng"]) <= max_distance
        ]

    # === 处理无候选情况 ===
    if not candidates_list:
        return jsonify([]), 200

    # === 非重复随机推荐 ===
    global _LAST_IDS
    result = sample_restaurants(candidates_list, k=1, exclude_ids=_LAST_IDS)

    if not result:
        _LAST_IDS = []
        result = sample_restaurants(candidates_list, k=1, exclude_ids=[])

    # === 加上距离字段 ===
    if user_lat and user_lng:
        d = plane_distance(user_lat, user_lng, result[0]["lat"], result[0]["lng"])
        result[0]["distance_km"] = round(d, 1)
    else:
        result[0]["distance_km"] = round(random.uniform(0.5, 3.0), 1)

    # 更新排除 ID
    rid = result[0]["id"]
    _LAST_IDS.append(rid)
    _LAST_IDS = _LAST_IDS[-_LAST_CAP:]

    return jsonify(result), 200
