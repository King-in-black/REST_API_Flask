def test_player_get_function_1(client):
        code = 'arnold'
        response = client.get(f'/get/get_player/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['Player_ID'] == 'arnold'


