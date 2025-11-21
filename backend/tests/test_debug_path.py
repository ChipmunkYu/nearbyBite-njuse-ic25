# tests/test_debug_path.py
# 用于调试 PYTHONPATH，测试模块导入是否成功（非功能性测试）
import sys
import os

def test_show_path():
    print("\nPYTHONPATH =")
    for p in sys.path:
        print("  ", p)

    try:
        from src.app.app import create_app
        print("\n 成功导入 create_app")
    except Exception as e:
        print("\n 导入失败：", e)
        assert False, "导入 app.app.create_app 失败"
