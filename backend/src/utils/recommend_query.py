# src/utils/recommend_query.py
import math
import random

def plane_distance(lat1, lng1, lat2, lng2):
    """平面近似距离，南京地区经验值"""
    K = 0.85
    dx = (lng2 - lng1) * K
    dy = (lat2 - lat1) * K
    return math.sqrt(dx * dx + dy * dy)

def sample_restaurants(candidates: list, k=1, exclude_ids=None):
    """随机选不重复餐馆"""
    if not candidates:
        return []

    exclude_ids = set(exclude_ids or [])
    fresh = [r for r in candidates if r["id"] not in exclude_ids]

    if len(fresh) >= k:
        return random.sample(fresh, k)

    chosen = list(fresh)
    remaining = [r for r in candidates if r not in chosen]
    need = k - len(chosen)

    if remaining:
        chosen.extend(random.sample(remaining, min(len(remaining), need)))

    return chosen
