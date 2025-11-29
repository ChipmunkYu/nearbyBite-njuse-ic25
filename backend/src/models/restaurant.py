from datetime import datetime
from src.extensions import db


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 你明确要求要保留的字段
    name = db.Column(db.String(100), nullable=False)
    avg_price = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.JSON, nullable=True)     # ["快餐", "人均30"]

    # 与爬虫结果对应（可为空）
    address = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    source = db.Column(db.String(50), nullable=True)
    last_crawled_time = db.Column(db.DateTime, nullable=True)

    # 管理字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"

    @staticmethod
    def from_crawler_data(data: dict):
        """ 将爬虫 parse_poi 输出的数据转成模型实例 """
        return Restaurant(
            name=data.get("name"),
            address=data.get("address"),
            latitude=data.get("lat"),
            longitude=data.get("lng"),
            avg_price=data.get("price"),
            rating=data.get("rating"),
            source=data.get("source", "amap"),
            last_crawled_time=datetime.fromisoformat(
                data.get("last_crawled_time")
            ) if data.get("last_crawled_time") else None,
        )