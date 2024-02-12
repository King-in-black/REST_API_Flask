from ..extension import db, ma
from ..models import Player, Trainer, Data
from sqlalchemy import func


def test_player_delete_function_1(client, player_json_a):
    response1 = client.post("/post/player_add", json=player_json_a)
    code = "arnold"
    response2 = client.get(f"/get/get_player/{code}")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data["Player_ID"] == "arnold"
    response3 = client.delete("/delete/delete_player", json=player_json_a)
    assert response3.status_code == 201


def test_player_delete_function_2(client, player_json_a):
    response1 = client.post("/post/player_add", json=player_json_a)
    code = "arnold"
    response2 = client.get(f"/get/get_player/{code}")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data["Player_ID"] == "arnold"
    response3 = client.delete("/delete/delete_player", json=player_json_a)
    assert response3.status_code == 201
    response4 = client.delete("/delete/delete_player", json=player_json_a)
    assert response4.status_code == 409


def test_trainer_get_function_1(client, trainer_json_a):
    response1 = client.post("/post/trainer_add", json=trainer_json_a)
    code = "a"
    response2 = client.get(f"/get/get_trainer/{code}")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data["Trainer_ID"] == "a"
    response3 = client.delete("/delete/delete_trainer", json=trainer_json_a)
    assert response3.status_code == 201


def test_trainer_get_function_2(client, trainer_json_a):
    response1 = client.post("/post/trainer_add", json=trainer_json_a)
    code = "a"
    response2 = client.get(f"/get/get_trainer/{code}")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data["Trainer_ID"] == "a"
    response3 = client.delete("/delete/delete_trainer", json=trainer_json_a)
    assert response3.status_code == 201
    response4 = client.delete("/delete/delete_trainer", json=trainer_json_a)
    assert response4.status_code == 409


def test_data(client, data_row_json):
    response1 = client.post("/post/Datarow_add", json=data_row_json)
    code = db.session.query(func.max(Data.Data_ID)).scalar()
    response2 = client.get(f"/get/Datarow_get/{code}")
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert json_data["accX"] == 1
    assert json_data["accY"] == 1
    assert json_data["accZ"] == 1
    response3 = client.delete(f"/delete/delete_datarow/{code}")
    assert response3.status_code == 201
    response4 = client.delete(f"/delete/delete_datarow/{code}")
    assert response4.status_code == 409
