# backend/src/scripts/seed.py

"""
Seed script for initializing the database with sample restaurant data.
Usage:
    python -m src.scripts.seed
"""

from src.app.app import create_app
from src.extensions import db
from src.models.restaurant import Restaurant

from datetime import datetime


def seed_restaurants():
    """Insert sample restaurant data (20–30 entries)."""

    sample_data = [
        {
            "name": "麦当劳 中山路店",
            "avg_price": 30,
            "tags": ["快餐", "人均30"],
            "address": "南京市中山路100号",
            "rating": 4.2,
        },
        {
            "name": "肯德基 新街口店",
            "avg_price": 32,
            "tags": ["快餐", "人均30"],
            "address": "南京市淮海路88号",
            "rating": 4.1,
        },
        {
            "name": "西贝莜面村",
            "avg_price": 60,
            "tags": ["中餐", "西北菜"],
            "address": "南京市鼓楼区中央路50号",
            "rating": 4.5,
        },
        {
            "name": "海底捞 火锅 银泰店",
            "avg_price": 120,
            "tags": ["火锅", "连锁"],
            "address": "南京市建邺区江东中路",
            "rating": 4.8,
        },
        {
            "name": "小杨生煎 新街口店",
            "avg_price": 25,
            "tags": ["小吃"],
            "address": "南京市中山东路",
            "rating": 4.3,
        },
        # 你可以根据需要继续复制扩展到 20～30 条
    ]

    # 自动补齐 created_at 等字段
    for item in sample_data:
        item["source"] = "manual"
        item["last_crawled_time"] = datetime.utcnow()

    for item in sample_data:
        r = Restaurant(**item)
        db.session.add(r)

    db.session.commit()
    print(f"插入 {len(sample_data)} 条餐馆数据成功！")


def run():
    app = create_app()

    with app.app_context():
        print("清空数据库...")
        db.drop_all()

        print("创建数据库表...")
        db.create_all()

        print("写入示例餐馆数据...")
        seed_restaurants()

        print("Seed 完成！")


if __name__ == "__main__":
    run()
