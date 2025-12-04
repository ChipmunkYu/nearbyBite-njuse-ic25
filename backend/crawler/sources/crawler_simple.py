# backend/crawler/sources/crawler_simple.py
import requests
import json
from datetime import datetime
import os
import sys

# ----------------------------
# 让爬虫可以找到 backend 包
# ----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(BACKEND_DIR)

# from src.app.app import create_app
from src.extensions import db
from src.models.restaurant import Restaurant

# # ----------------------------
# # 初始化 Flask App Context
# app = create_app()
# app.app_context().push()

# ----------------------------
# 高德 API KEY
# ----------------------------
AMAP_KEY = "d7136435e934f09f79ce84e8ae79f0c2"


def fetch_from_amap():
    """
    调用高德 Web API，获取南京“美食”类餐馆。
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "keywords": "美食",
        "city": "南京",
        "output": "json",
        "key": AMAP_KEY,
        "page": 1,
        "offset": 5,  # 测试用 5 条
    }

    print("正在请求高德 API ...")
    resp = requests.get(url, params=params)
    data = resp.json()

    # 调试时可以保留打印，之后可以注释掉
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return data


def parse_poi(poi):
    """
    将高德POI结构解析成最简版餐馆字典。
    """
    name = poi.get("name")
    address = poi.get("address")

    # 经纬度
    location = poi.get("location", "")
    try:
        lat_str, lng_str = location.split(",")
        lat = float(lat_str)
        lng = float(lng_str)
    except Exception:
        lat, lng = None, None

    # 评分与人均
    biz = poi.get("biz_ext", {})
    rating_raw = biz.get("rating")
    price_raw = biz.get("cost")

    try:
        rating = float(rating_raw) if rating_raw else None
    except Exception:
        rating = None

    try:
        price = int(float(price_raw)) if price_raw else None
    except Exception:
        price = None

    return {
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "price": price,
        "rating": rating,
        "source": "amap",
        "last_crawled_time": datetime.now().isoformat(),
    }


def create_or_update_restaurant(data):
    """
    根据 name + address 去重，如果存在则更新，否则新增。
    """
    name = data.get("name")
    address = data.get("address")

    existing = Restaurant.query.filter_by(name=name, address=address).first()

    if existing:
        existing.latitude = data["lat"]
        existing.longitude = data["lng"]
        existing.avg_price = data["price"]
        existing.rating = data["rating"]
        existing.source = data["source"]
        existing.last_crawled_time = datetime.fromisoformat(
            data["last_crawled_time"]
        )
        db.session.commit()
        return "update"

    new_r = Restaurant.from_crawler_data(data)
    db.session.add(new_r)
    db.session.commit()
    return "insert"


def run_crawler_main():
    """
    提供给定时任务调用的主流程：
    1. 请求高德
    2. 解析 POI
    3. 入库（insert/update）
    """
    # ✅ 在函数内部导入，避免循环
    from src.app.app import create_app
    
    # 创建应用和上下文
    app = create_app()
    with app.app_context():

        print("🐍 爬虫使用的数据库 =", db.engine.url)
        raw = fetch_from_amap()
        pois = raw.get("pois", [])
        print(f"\n[爬虫] 共获取 {len(pois)} 条数据\n")

        parsed_list = [parse_poi(p) for p in pois]

        for item in parsed_list:
            result = create_or_update_restaurant(item)
            print(f"[爬虫] {item['name']} → {result}")

        print("\n[爬虫] 本次运行完成！")


if __name__ == "__main__":
    # 手动运行脚本时，也走同一套流程
    run_crawler_main()