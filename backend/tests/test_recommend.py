# test/test_recommend.py
# 测试 `/restaurants/recommend` 推荐接口返回数据结构与字段正确

def test_recommend_basic(client):
    response = client.get("/api/recommend/restaurants")
    #可访问性
    assert response.status_code == 200  

    data = response.get_json()
     #结构是列表
    assert isinstance(data, list)      
    #至少推荐一个结果
    assert len(data) > 0                

    #字段完整性
    for item in data:
        assert isinstance(item, dict)
        assert "name" in item
        assert "location" in item
        assert "tags" in item           
    #数据类型合理性
        assert isinstance(item["name"], str)
        assert isinstance(item["location"], str)
        assert isinstance(item["tags"], list)  


# 因为router里面还是很基础的版本，所以没有测试推荐是否正确
# TODO：完善推荐算法后，补充推荐正确性的测试