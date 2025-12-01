# src/models/history.py
# 功能：定义 History 数据表，用于记录用户的餐馆浏览记录

from datetime import datetime,  timezone
from ..extensions import db

def utc_now():
    return datetime.now(timezone.utc)

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   # 可改 int
    restaurant_name = db.Column(db.String(128), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=utc_now)
    dishes_info = db.Column(db.JSON, nullable=True)
    # 可扩展字段：restaurant_detail
    # restaurant_detail = db.Column(db.JSON, nullable=True)
    restaurant = db.relationship('Restaurant', backref='histories')
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_name": self.restaurant_name,
            "restaurant_id": self.restaurant_id,
            "timestamp": self.timestamp.isoformat(),
            "dishes_info": self.dishes_info
        }