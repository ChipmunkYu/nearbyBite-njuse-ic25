import requests
import json
from datetime import datetime

AMAP_KEY = "d7136435e934f09f79ce84e8ae79f0c2"
def fetch_from_amap():
    """
    调用高德 Web API,获取南京市“美食”类 POI 的最简示例。
    """
    url = "https://restapi.amap.com/v3/place/text"

    params = {
        "keywords": "美食",
        "city": "南京",
        "output": "json",
        "key": AMAP_KEY,
        "page": 1,
        "offset": 5  # 每页返回 5 条，最简测试
    }

    print("正在请求高德 API ...")

    resp = requests.get(url, params=params)
    data = resp.json()

    # 打印结构化结果
    print(json.dumps(data, indent=2, ensure_ascii=False))

    return data

def parse_poi(poi):
    """
    将高德POI结构解析成最简版餐馆字典。
    """
    # name & address
    name = poi.get("name")
    address = poi.get("address")

    # location（经纬度）
    location = poi.get("location", "")
    try:
        lat_str, lng_str = location.split(",")
        lat = float(lat_str)
        lng = float(lng_str)
    except Exception:
        lat, lng = None, None  # 最简容错
 
    # rating & cost（人均）
    biz = poi.get("biz_ext", {})
    rating_raw = biz.get("rating")
    price_raw = biz.get("cost")

    # 转换 rating → float
    try:
        rating = float(rating_raw) if rating_raw else None
    except:
        rating = None

    # 转换 price → int
    try:
        price = int(float(price_raw)) if price_raw else None
    except:
        price = None

    return {
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "price": price,
        "rating": rating,
        "source": "amap",
        "last_crawled_time": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Step 1：请求高德 API
    data = fetch_from_amap()

    # Step 2：获取 POI 列表
    pois = data.get("pois", [])
    print(f"\n共获取 {len(pois)} 条原始POI数据")

    # Step 3：解析第一条作为示例
    if pois:
        parsed = parse_poi(pois[0])
        print("\n解析后的最简数据示例：")
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print("没有获得 POI 数据")
