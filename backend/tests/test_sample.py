# backend/tests/test_sample.py

def test_basic_math():
    """简单数学运算测试（确认 pytest 运行正常）"""
    assert 1 + 1 == 2

def test_string_check():
    """字符串匹配测试"""
    s = "nearbyBite"
    assert "Bite" in s
