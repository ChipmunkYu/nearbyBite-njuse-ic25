# backend/src/routes/stats.py
from flask import Blueprint, jsonify
from src.models.history import History
from src.models.restaurant import Restaurant
from src.models.user import User
from src.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone

stats_bp = Blueprint("stats", __name__, url_prefix="/api/users")


@stats_bp.get("/me/stats")
@jwt_required()
def get_my_stats():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    # 历史 + 餐馆 JOIN
    records = (
        db.session.query(History, Restaurant)
        .join(Restaurant, Restaurant.id == History.restaurant_id)
        .filter(History.user_id == uid)
        .all()
    )

    if not records:
        return jsonify({
            "code": 200,
            "message": "OK",
            "data": {
                "total_visits": 0,
                "avg_price": None,
                "cuisine_counts": {},
                "top_cuisines": [],
                "price_buckets": {},
                "daily_visits": [],
                "top_restaurants": [],
                "unique_restaurants": 0,
            }
        })

    total_visits = len(records)

    # --------- 平均价位 + 价位分布 ----------
    price_sum = 0
    price_count = 0
    price_buckets = {
        "0-20": 0,
        "20-40": 0,
        "40-60": 0,
        "60+": 0,
    }

    # --------- 菜系分布 ----------
    cuisine_counts = {}

    # --------- 每家餐馆访问次数 ----------
    restaurant_visit_counts = {}  # rest_id -> count
    restaurant_info = {}          # rest_id -> (name, avg_price, tags)

    # --------- 最近 7 天访问 ----------
    # 先按日期字符串计数
    daily_counts = {}  # "YYYY-MM-DD" -> count

    for history, restaurant in records:
        if not restaurant:
            continue

        # 价位
        if restaurant.avg_price is not None:
            p = restaurant.avg_price
            price_sum += p
            price_count += 1

            if p < 20:
                price_buckets["0-20"] += 1
            elif p < 40:
                price_buckets["20-40"] += 1
            elif p < 60:
                price_buckets["40-60"] += 1
            else:
                price_buckets["60+"] += 1

        # 菜系 tags（过滤带数字的标签，例如“人均30”）
        if restaurant.tags:
            for tag in restaurant.tags:
                if any(ch.isdigit() for ch in tag):
                    continue
                cuisine_counts[tag] = cuisine_counts.get(tag, 0) + 1

        # 餐馆访问次数
        rid = restaurant.id
        restaurant_visit_counts[rid] = restaurant_visit_counts.get(rid, 0) + 1
        restaurant_info[rid] = (
            restaurant.name,
            restaurant.avg_price,
            restaurant.tags
        )

        # 日期统计
        if history.timestamp:
            # 确保是 aware datetime，如果你存的是 UTC，就按 UTC 算
            dt = history.timestamp
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            date_str = dt.date().isoformat()
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1

    # 平均价位
    avg_price = round(price_sum / price_count, 2) if price_count else None

    # Top3 菜系（已有逻辑）
    top_cuisines = sorted(
        cuisine_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    # Top N 常去餐馆（这里取前 5）
    top_restaurants = []
    for rid, cnt in sorted(restaurant_visit_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        name, ap, tags = restaurant_info.get(rid, ("未知餐馆", None, []))
        top_restaurants.append({
            "name": name,
            "count": cnt,
            "avg_price": ap,
            "tags": tags or []
        })

    # 最近 7 天日期列表
    today = datetime.now(timezone.utc).date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_visits = [
        {
            "date": d.isoformat(),
            "count": daily_counts.get(d.isoformat(), 0)
        }
        for d in last_7_days
    ]

    unique_restaurants = len(restaurant_visit_counts)

    return jsonify({
        "code": 200,
        "message": "OK",
        "data": {
            "total_visits": total_visits,
            "avg_price": avg_price,
            "cuisine_counts": cuisine_counts,
            "top_cuisines": top_cuisines,
            "price_buckets": price_buckets,
            "daily_visits": daily_visits,
            "top_restaurants": top_restaurants,
            "unique_restaurants": unique_restaurants,
        }
    })
