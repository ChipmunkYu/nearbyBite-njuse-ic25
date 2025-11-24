# src/app/recommend.py
import random
from flask import Blueprint, jsonify, request
from src.utils.recommend_query import filter_restaurants, sample_restaurants, plane_distance

recommend_bp = Blueprint("recommend", __name__, url_prefix="/api/recommend")

_LAST_IDS = []
_LAST_CAP = 10

@recommend_bp.route("/restaurants", methods=["GET"])
def recommend():

    # === 参数 ===
    price_min = request.args.get("price_min", 0, type=float)
    price_max = request.args.get("price_max", 200, type=float)
    min_rating = request.args.get("min_rating", None, type=float)
    area = request.args.get("area", "", type=str)

    types = [t for t in request.args.get("types", "", type=str).split(",") if t]
    flavors = [f for f in request.args.get("flavors", "", type=str).split(",") if f]

    max_distance = request.args.get("max_distance_km", None, type=float)
    user_lat = request.args.get("lat", None, type=float)
    user_lng = request.args.get("lng", None, type=float)

    filters = {
        "price_min": price_min,
        "price_max": price_max,
        "min_rating": min_rating,
        "area": area,
        "types": types,
        "flavors": flavors,
    }

    # ===  基础筛选 ===
    candidates = filter_restaurants(filters)

    # ===  处理距离限制 ===
    if user_lat and user_lng and max_distance:
        candidates = [
            r for r in candidates
            if plane_distance(user_lat, user_lng, r["lat"], r["lng"]) <= max_distance
        ]

    # ===  非重复随机选1 ===
    global _LAST_IDS
    result = sample_restaurants(candidates, k=1, exclude_ids=_LAST_IDS)

    if not result:
        # 无候选或被排除光了
        if not candidates:
            return jsonify([]), 200
        _LAST_IDS = []
        result = sample_restaurants(candidates, k=1, exclude_ids=[])

    # ===  给前端距离字段 ===
    if user_lat and user_lng:
        d = plane_distance(user_lat, user_lng, result[0]["lat"], result[0]["lng"])
        result[0]["distance_km"] = round(d, 1)
    else:
        # 无定位 → 给伪距离
        result[0]["distance_km"] = round(random.uniform(0.2, 3.5), 1)

    # === 6. 更新缓存 ===
    rid = result[0]["id"]
    _LAST_IDS.append(rid)
    _LAST_IDS = _LAST_IDS[-_LAST_CAP:]

    return jsonify(result), 200
