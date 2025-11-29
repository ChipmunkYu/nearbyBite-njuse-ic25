#建新表记得在此处引入模型
from .user import User
from .history import History
from .restaurant import Restaurant

__all__ = [
    "User",
    "History",
    "Restaurant",
]