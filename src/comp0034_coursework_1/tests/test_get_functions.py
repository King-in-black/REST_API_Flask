from ..extension import db,ma
from ..models import Player,Trainer,Data
from sqlalchemy import func
def test_player_get_function_1(client,player_json_a):
        response = client.post(
                '/post/player_add',
                json=player_json_a
        )
        code = 'arnold'
        response = client.get(f'/get/get_player/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['Player_ID'] == 'arnold'

def test_player_get_function_2(client,player_json_b):
        response = client.post(
                '/post/player_add',
                json=player_json_b
        )
        code = 'bill'
        response = client.get(f'/get/get_player/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['Player_ID'] == 'bill'

def test_trainer_get_function_1(client,trainer_json_a):
        response = client.post(
                '/post/trainer_add',
                json=trainer_json_a
        )
        code = 'a'
        response = client.get(f'/get/get_trainer/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['Trainer_ID'] == 'a'

def test_trainer_get_function_2(client,trainer_json_b):
        response = client.post(
                '/post/trainer_add',
                json=trainer_json_b
        )
        code = 'b'
        response = client.get(f'/get/get_trainer/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['Trainer_ID'] == 'b'

def test_data(client,data_row_json):
        response = client.post(
                '/post/Datarow_add',
                json=data_row_json
        )
        code= db.session.query(func.max(Data.Data_ID)).scalar()
        response = client.get(f'/get/Datarow_get/{code}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['accX'] == 1
        assert json_data['accY'] == 1
        assert json_data['accZ'] == 1

def test_get_player_through_trainer_ID(client,player_json_c):
        response1=client.post('post/player_add',
                              json=player_json_c)
        assert  response1.status_code ==201
        response2 =client.get('get/get_player_t/a')
        assert  response2.status_code == 200
        json_data = response2.get_json()
        assert  json_data[0]['Player_ID'] == 'arnold'
        assert  json_data[0]['Trainer_ID'] == 'a'
        assert  json_data[1]['Player_ID'] == 'cat'
        assert  json_data[1]['Trainer_ID'] == 'a'

