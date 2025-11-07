# src/models/history.py
# 功能：定义 History 数据表，用于记录用户的餐馆浏览记录

from datetime import datetime
from ..extensions import db

class History(db.Model):
    """
    历史记录（浏览记录）模型：
    - 当用户点击/查看某个餐馆时，写入数据库
    """
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)               # 主键
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # 用户外键
    restaurant_name = db.Column(db.String(100), nullable=False)  # 浏览的餐馆名称（若未来有餐馆表可改为 restaurant_id）
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 浏览时间（自动记录当前时间）

    def to_dict(self):
        """用于返回给前端的 JSON 数据格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_name": self.restaurant_name,
            "timestamp": self.timestamp.isoformat()
        }
