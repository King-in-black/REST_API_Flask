
from ..models import Data,Trainer,Player
from ..extension import db
def test_player_post_function_1(client,player_json_a):
    '''
    This is the first test function
    Ensure the test_database does not have the record first
    the function asks to import a json file of a player to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    :param client: the test client
    '''
    response=client.post(
        '/post/player_add',
        json = player_json_a
    )
    print(response.json)
    assert response.status_code == 201
    obj2 = db.session.execute(db.select(Player).filter_by(Player_ID='arnold', password='********',Trainer_ID='a')).scalar()
    assert obj2 != None
def test_player_post_function_2(client,player_json_b,app):
    '''
    This is the second test for the function.
    Ensure the test_database have the same  record first
    the function asks to import a json file of a player to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    It should return a failure status.
    :param client: the test client
    '''
    response1=client.post(
        '/post/player_add',
        json = player_json_b
    )
    response2 = client.post(
        '/post/player_add',
        json= player_json_b
    )
    # not sure whether it is 404 or not
    assert response2.status_code == 201

def test_trainer_post_function_1(client,trainer_json_a):
    '''
    This is the first test for the function.
    the function asks to import a json file of a trainer to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    :param client: the test client
    '''
    response = client.post(
        '/post/trainer_add',
        json=trainer_json_a
    )
    assert response.data != None
    assert response.status_code == 201
    obj2 = db.session.execute(db.select(Trainer).filter_by(Trainer_ID='a', password='********')).scalar()
    assert obj2 != None
def test_trainer_post_function_2(client,trainer_json_b):
    '''
    This is the second test for the function.
    Ensure the test_database have the same  record first
    the function asks to import a json file of a trainer to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    It should return a failure status.
    :param client: the test client
    '''
    response=client.post(
        '/post/trainer_add',
        json = trainer_json_b
    )
    response = client.post(
        '/post/trainer_add',
        json= trainer_json_b
    )
    # not sure whether it is 404 or not
    assert response.status_code == 201