# 备注：这是餐馆数据模型（占位版）。负责餐馆数据的同学在这里补全/修改字段即可。

from src.extensions import db

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)

    # 基础字段（可根据实际数据修改）
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    area = db.Column(db.String(50))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)

    # 标签字段（格式占位，可改）
    types = db.Column(db.String(200))
    flavors = db.Column(db.String(200))

    # 经纬度（高德爬下来的坐标填这里）
    lat = db.Column(db.Float)
    lng = db.Column(db.Float) 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "area": self.area,
            "price": self.price,
            "rating": self.rating,
            "types": self.types.split(",") if self.types else [],
            "flavors": self.flavors.split(",") if self.flavors else [],
            "lat": self.lat,
            "lng": self.lng,
        }
