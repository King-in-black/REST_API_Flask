def test_player_get_function_1(client):
        code = 'arnold'
        response = client.get(f'/get_player/{code}')
        assert response.status_code == 200

        # 如果返回的是 JSON 数据，验证响应数据的结构和内容是否正确
        # 这里的 'name' 和 'info' 取决于您实际返回的 JSON 结构
        json_data = response.get_json()
        assert json_data['Player_ID'] == 'arnold'  # 举例，假设返回的信息中应包含国家名
        assert 'info' in json_data  # 假设 JSON 应该包含 'info' 字段

        # 根据实际情况可能需要添加更多的断言

