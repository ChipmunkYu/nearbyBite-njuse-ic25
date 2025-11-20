# src/models/history.py
# 功能：定义 History 数据表，用于记录用户的餐馆浏览记录

from datetime import datetime
from ..extensions import db

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)   # 可改 int
    restaurant_name = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 可扩展字段：restaurant_detail
    # restaurant_detail = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_name": self.restaurant_name,
            "timestamp": self.timestamp.isoformat(),
        }