# backend/tests/conftest.py

import sys
import os
import pytest

#其余test文件不需要加下面一行。因为windows系统比较保守，pytest.ini里面的文件老是不起作用，因此将 backend/src 添加到模块搜索路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
