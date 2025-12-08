# src/routes/restaurants.py
#待加jwt验证
from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.restaurant import Restaurant
from flask_jwt_extended import jwt_required
restaurants_bp = Blueprint("restaurants", __name__, url_prefix="/api/restaurants")


@restaurants_bp.get("")
@jwt_required()
def get_restaurants():
    """GET /api/restaurants?page=1&size=10"""
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))

    query = Restaurant.query
    total = query.count()
    records = query.offset((page - 1) * size).limit(size).all()

    return jsonify({
        "code": 200,
        "total": total,
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "address": r.address,
                "avg_price": r.avg_price,
                "rating": r.rating,
                "tags": r.tags,
            }
            for r in records
        ]
    })


@restaurants_bp.post("")
@jwt_required()
def create_restaurant():
    data = request.json
    r = Restaurant(
        name=data.get("name"),
        avg_price=data.get("avg_price"),
        tags=data.get("tags"),
        address=data.get("address"),
        rating=data.get("rating"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        source="manual"
    )
    db.session.add(r)
    db.session.commit()

    return jsonify({"code": 200, "message": "创建成功", "id": r.id})


@restaurants_bp.put("/<int:rest_id>")
@jwt_required()
def update_restaurant(rest_id):
    r = Restaurant.query.get_or_404(rest_id)
    data = request.json

    r.name = data.get("name", r.name)
    r.avg_price = data.get("avg_price", r.avg_price)
    r.tags = data.get("tags", r.tags)
    r.address = data.get("address", r.address)
    r.rating = data.get("rating", r.rating)
    r.latitude = data.get("latitude", r.latitude)
    r.longitude = data.get("longitude", r.longitude)

    db.session.commit()
    return jsonify({"code": 200, "message": "更新成功"})


@restaurants_bp.delete("/<int:rest_id>")
@jwt_required()
def delete_restaurant(rest_id):
    r = Restaurant.query.get_or_404(rest_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"code": 200, "message": "删除成功"})
