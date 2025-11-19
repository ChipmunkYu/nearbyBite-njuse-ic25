# 定义数据库模型(User)
import random
import string
from datetime import datetime
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

def generate_account_number(k = 8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k = k))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(20), unique = True, nullable = False)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    #这里采用 UTC 时间存储，确保时间的一致性，需要显示的时候转换为本地时间即可
    created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }