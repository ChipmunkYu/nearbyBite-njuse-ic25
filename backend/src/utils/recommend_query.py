# 推荐模块的数据库查询构建函数

from src.models.restaurant import Restaurant

def build_restaurant_query(filters):
    """
    根据筛选条件构建 SQLAlchemy 查询。
    """
    query = Restaurant.query

    # 价格
    if filters.get("price_min") is not None:
        query = query.filter(Restaurant.price >= filters["price_min"])
    if filters.get("price_max") is not None:
        query = query.filter(Restaurant.price <= filters["price_max"])

    # 评分
    if filters.get("min_rating") is not None:
        query = query.filter(Restaurant.rating >= filters["min_rating"])

    # 地区
    if filters.get("area"):
        query = query.filter(Restaurant.area == filters["area"])

    # 类型
    if filters.get("types"):
        for t in filters["types"]:
            query = query.filter(Restaurant.types.like(f"%{t}%"))

    # 口味
    if filters.get("flavors"):
        for f in filters["flavors"]:
            query = query.filter(Restaurant.flavors.like(f"%{f}%"))

    return query