#backend/src/routes/stats.py
from flask import Blueprint, jsonify
from src.models.history import History
from src.models.restaurant import Restaurant

stats_bp = Blueprint("stats", __name__, url_prefix="/api/users")


@stats_bp.get("/<int:user_id>/stats")
def get_stats(user_id):
    """基础版统计接口：常点价位 + 常点菜系"""
    records = History.query.filter_by(user_id=user_id).all()

    price_counts = {}
    cuisine_counts = {}

    for h in records:
        r = Restaurant.query.get(h.restaurant_id)
        if not r:
            continue

        # price
        if r.avg_price:
            price_counts[r.avg_price] = price_counts.get(r.avg_price, 0) + 1

        # tags 中可能有菜系
        if r.tags:
            for tag in r.tags:
                cuisine_counts[tag] = cuisine_counts.get(tag, 0) + 1

    return jsonify({
        "code": 200,
        "price_stats": price_counts,
        "cuisine_stats": cuisine_counts
    })
