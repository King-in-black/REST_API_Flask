from ..extension import db, ma
from ..models import Player, Trainer, Data
from sqlalchemy import func


def test_player_get_function_1(client, player_json_a):
    """
    Post the content of a player first, and get the json file from the database
    param:
          client: the test client
          player_json_a: the json file defined in conftest.py
    """
    response = client.post("/post/player_add", json=player_json_a)
    code = "arnold"
    response = client.get(f"/get/get_player/{code}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["Player_ID"] == "arnold"


def test_player_get_function_2(client, player_json_b):
    """
    Post the content of a player first, and get the json file from the database. The second json file is tested with a
    different json file
    param:
          client: the test client
          player_json_b: the json file defined in conftest.py
    """
    response = client.post("/post/player_add", json=player_json_b)
    code = "bill"
    response = client.get(f"/get/get_player/{code}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["Player_ID"] == "bill"


def test_trainer_get_function_1(client, trainer_json_a):
    """
    Post the content of a trainer first, and get the json file from the database.
    param:
      client: the test client
      trainer_json_a: the json file defined in conftest.py
    """
    response = client.post("/post/trainer_add", json=trainer_json_a)
    code = "a"
    response = client.get(f"/get/get_trainer/{code}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["Trainer_ID"] == "a"


def test_trainer_get_function_2(client, trainer_json_b):
    """
        Post the content of a trainer first, and get the json file from the database.
        The second json file is tested with a different json file
    param:
      client: the test client
      trainer_json_b: the json file defined in conftest.py
    """
    response = client.post("/post/trainer_add", json=trainer_json_b)
    code = "b"
    response = client.get(f"/get/get_trainer/{code}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["Trainer_ID"] == "b"


def test_data(client, data_row_json):
    """
    Post the content of a row of the data first, and get the json file from the database.
    the code is the maximum number of data_ID. Data_ID is the primary key of the datarow and
    it is self-increasing.
    param:
      client: the test client
      data_row_json: the json file defined in conftest.py
    """
    response = client.post("/post/Datarow_add", json=data_row_json)
    code = db.session.query(func.max(Data.Data_ID)).scalar()
    response = client.get(f"/get/Datarow_get/{code}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["accX"] == 1
    assert json_data["accY"] == 1
    assert json_data["accZ"] == 1


def test_get_player_through_trainer_ID(client, player_json_c):
    """
    The test functions allow players to check which players are connected to the train a.
    The system will post 2 players first. The json player arnold has already defined before.
    Therefore, only json player cat will be defined.
          param:
          client: the test client
          data_row_json: the json file defined in conftest.py
    """
    response1 = client.post("post/player_add", json=player_json_c)
    assert response1.status_code == 201
    response2 = client.get("get/get_player_t/a")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data[0]["Player_ID"] == "arnold"
    assert json_data[0]["Trainer_ID"] == "a"
    assert json_data[1]["Player_ID"] == "cat"
    assert json_data[1]["Trainer_ID"] == "a"
