# src/app/recommend_query.py
"""
推荐页后端：伪数据 + 筛选 + 距离伪造 + 非重复抽样

功能点：
1. 提供 mock 餐馆数据（含 lat/lng）
2. 支持多选菜系、多选口味
3. 支持价格区间 price_min~price_max
4. 支持地区 area
5. 支持评分 min_rating
6. 支持伪距离（前端 max_distance_km）
7. 支持"避免重复推荐"的随机算法
"""

import random
import math

# ====================== 假数据 ======================

mock_restaurants = [
    # --- 鼓楼 ---
    {
        "id": 1, "name": "麦当劳（鼓楼）", "location": "广州路", "area": "鼓楼",
        "price": 30, "rating": 4.2, "types": ["快餐"], "flavors": ["咸香"],
        "lat": 32.0565, "lng": 118.7792
    },
    {
        "id": 2, "name": "兰州拉面（鼓楼）", "location": "汉口路", "area": "鼓楼",
        "price": 22, "rating": 4.0, "types": ["小吃"], "flavors": ["咸香"],
        "lat": 32.0593, "lng": 118.7800
    },
    {
        "id": 3, "name": "蜜雪冰城（鼓楼）", "location": "百子亭", "area": "鼓楼",
        "price": 10, "rating": 4.5, "types": ["奶茶"], "flavors": ["甜"],
        "lat": 32.0605, "lng": 118.7780
    },

    # --- 仙林 ---
    {
        "id": 7, "name": "海底捞（仙林）", "location": "大学城", "area": "仙林",
        "price": 95, "rating": 4.8, "types": ["火锅"], "flavors": ["辣", "重口味"],
        "lat": 32.1264, "lng": 118.9459
    },
    {
        "id": 8, "name": "烤匠（仙林）", "location": "仙林中心", "area": "仙林",
        "price": 60, "rating": 4.5, "types": ["烧烤"], "flavors": ["麻辣", "重口味"],
        "lat": 32.1248, "lng": 118.9485
    },

    # --- 新街口 ---
    {
        "id": 14, "name": "胖哥俩肉蟹煲（新街口）", "location": "新街口", "area": "新街口",
        "price": 78, "rating": 4.7, "types": ["川菜"], "flavors": ["麻辣"],
        "lat": 32.0402, "lng": 118.7890
    },
    {
        "id": 15, "name": "炉鱼（新街口）", "location": "新街口", "area": "新街口",
        "price": 88, "rating": 4.6, "types": ["烤鱼"], "flavors": ["麻辣", "重口味"],
        "lat": 32.0396, "lng": 118.7912
    },
]


# ====================== 计算距离 ======================

def plane_distance(lat1, lng1, lat2, lng2):
    K = 0.85  # 经验值：1度 ≈ 0.85 km（南京纬度）
    dx = (lng2 - lng1) * K
    dy = (lat2 - lat1) * K
    return math.sqrt(dx * dx + dy * dy)


# ====================== 筛选函数 ======================

def filter_restaurants(filters: dict):
    """
    按筛选条件（价格/类型/口味/地区/评分）过滤。
    距离不在这里筛选（伪距离在路由里生成）。
    """
    price_min = filters.get("price_min", 0)
    price_max = filters.get("price_max", 9999)
    min_rating = filters.get("min_rating")
    area = filters.get("area") or ""
    types = filters.get("types") or []
    flavors = filters.get("flavors") or []

    result = []

    for r in mock_restaurants:

        # 价格
        if not (price_min <= r["price"] <= price_max):
            continue

        # 评分
        if min_rating is not None and r["rating"] < min_rating:
            continue

        # 地区
        if area and area not in ["全部", "all", "undefined", "null"]:
            if r["area"] != area:
                continue

        # 类型（菜系）
        if types and not any(t in r["types"] for t in types):
            continue

        # 口味
        if flavors and not any(f in r["flavors"] for f in flavors):
            continue

        result.append(r)

    return result


# ====================== 非重复随机抽样 ======================

def sample_restaurants(candidates: list, k=1, exclude_ids=None):
    """从候选中随机抽 k 个，尽量不重复"""
    if not candidates:
        return []

    exclude_ids = set(exclude_ids or [])

    fresh = [r for r in candidates if r["id"] not in exclude_ids]

    if len(fresh) >= k:
        return random.sample(fresh, k)

    # 不够就把 fresh 用完，再从剩余随机补
    chosen = list(fresh)
    remaining = [r for r in candidates if r not in chosen]

    need = k - len(chosen)
    if remaining:
        chosen.extend(random.sample(remaining, min(len(remaining), need)))

    return chosen