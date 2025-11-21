#建新表记得在此处引入模型
from .user import User
from .history import History  # 新增历史模型
#这里可以定义该模块对外暴露的接口，记得添加新模型
__all__ = ['User', 'History']
