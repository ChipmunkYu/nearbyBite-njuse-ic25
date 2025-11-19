# 后端项目说明

大致有一个结构，有和其它部分有连接的块可以大致说明一下

## 项目目录结构

## 目录结构说明

### config 目录 
存放配置文件

- test_config.py - 测试配置文件


### src 目录

#### app

- app.py - Flask 应用主入口
- app.db - SQLite 数据库文件
- '__init__.py' - 包初始化

#### models
存放数据模型，定义数据库表结构和业务实体

- user.py - 用户模型定义(User表)
- '__init__.py' - 包初始化
- history.py - 历史记录模型

#### routes
存放路由处理函数
放在这里让app.py干净一点

- auth.py - 用户注册、登录接口（/auth/register, /auth/login）
- history.py - 历史记录接口：查询/删除记录

#### utils
存放工具函数和辅助类，业务逻辑无关的通用功能

#### extensions.py
扩展配置


### test目录

- conftest.py 
- test_app.py 
- test_debug_path.py 
- test_recommend.py 
- test_sample.py 
-test_history.py
### requirements.txt

Python 依赖包列表

### pytest.ini
 
## 大致使用说明（bash）

安装依赖
pip install -r requirements.txt
（如果怕污染的话可以先弄一个虚拟环境，喂给AI会教的）

配置环境变量（.env文件）
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
JWT_SECRET_KEY=your_secret_key（可以用python随机生成一串）

启动 Flask 应用：
python -m src.app.app