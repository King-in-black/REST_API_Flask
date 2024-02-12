from ..models import Data, Trainer, Player
from ..extension import db
from sqlalchemy import func


def test_player_put_function_1(client, player_json_a):
    """
    Test to change the password of player
     :param client: the test client
            player_json_a: the json file defined in conftest.py
    """
    response1 = client.post("/post/player_add", json=player_json_a)
    print(response1.json)
    assert response1.status_code == 201
    obj1 = db.session.execute(
        db.select(Player).filter_by(
            Player_ID="arnold", password="********", Trainer_ID="a"
        )
    ).scalar()
    assert obj1 != None
    response2 = client.put(
        "/put/player",
        json={"Player_ID": "arnold", "password": "************", "Trainer_ID": "a"},
    )
    assert response2.status_code == 201
    obj2 = db.session.execute(
        db.select(Player).filter_by(
            Player_ID="arnold", password="************", Trainer_ID="a"
        )
    ).scalar()
    assert obj2 != None


def test_trainer_put_function_1(client, trainer_json_a):
    """
    Test to change the password of player
    :param client: the test client
            trainer_json_a: the json file defined in conftest.py
    """
    response1 = client.post("/post/trainer_add", json=trainer_json_a)
    print(response1.json)
    assert response1.status_code == 201
    obj1 = db.session.execute(
        db.select(Trainer).filter_by(Trainer_ID="a", password="********")
    ).scalar()
    assert obj1 != None
    response2 = client.put(
        "/put/trainer", json={"Trainer_ID": "a", "password": "************"}
    )
    assert response2.status_code == 201
    obj2 = db.session.execute(
        db.select(Player).filter_by(Trainer_ID="a", password="************")
    ).scalar()
    assert obj2 != None


def test_data_put_function_1(client, data_row_json):
    """
    Test to change content of data_row
     :param client: the test client
            data_row_json: the json file defined in conftest.py
    """
    response1 = client.post("/post/Datarow_add", json=data_row_json)
    print(response1.json)
    assert response1.status_code == 201
    code = db.session.query(func.max(Data.Data_ID)).scalar()
    obj1 = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar()
    assert obj1 != None
    response2 = client.put(
        f"/put/datarow/{code}",
        json={
            "Dataset_ID": 2,
            "Player_ID": "arnold",
            "Trainer_ID": "a",
            "timestamp": 2.0,
            "accX": 2.0,
            "accY": 2.0,
            "accZ": 2.0,
            "gyroX": 2.0,
            "gyroY": 2.0,
            "gyroZ": 2.0,
            "Activity": False,
            "Resultant_Acc": 2.0,
            "Resultant_Gyro": 2.0,
            "Average_Speed": 2.0,
            "Average_rotational_speed": 2.0,
        },
    )
    #
    assert response2.status_code == 201
    obj2 = db.session.execute(
        db.select(Data).filter_by(Average_rotational_speed=2.0)
    ).scalar()
    assert obj2 != None
    assert obj2.Data_ID == code
