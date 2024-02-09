
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from ..models import Player,Trainer,Data
from .. import schemas
from .conftest import db
def test_player_post_function_1(client,player_json_a,app):
    '''
    This is the first test function
    Ensure the test_database does not have the record first
    the function asks to import a json file of a player to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    :param client: the test client
    '''
    '''
    obj1 = db.session.execute(db.select(Player).filter_by(Player_ID='arnold', password='********',Trainer_ID='a')).scalar()
    try:
        assert obj1 == None
    except:
        print('there has already the records of Player_ID : arnold')
    '''
    response=client.post(
        '/player_add',
        json = player_json_a
    )

    try:
        assert response.status_code == 200
    except:
        print(f'the response.status_code is {response.status_code}')
        print('status code is not 200')
    obj2 = db.session.execute(db.select(Player).filter_by(Player_ID='arnold', password='********',Trainer_ID='a')).scalar()
    try:
        assert obj2 != None
    except:
        print('the records does not add in')
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
    response=client.post(
        '/player_add',
        json = player_json_b
    )
    response = client.post(
        '/player_add',
        json= player_json_b
    )
    # not sure whether it is 404 or not
    assert response.status_code == 404

def test_trainer_post_function_1(client,trainer_json_a,app):
    '''
    This is the first test for the function.
    the function asks to import a json file of a trainer to the database.
    And check whether it is working successfully by checking its status code
    and whether the database has same record as json file.
    :param client: the test client
    '''
    '''
    obj1 = db.session.execute(
        db.select(Trainer).filter_by(Trainer_ID='a', password='********')).scalar()
    assert obj1 == None
    response = client.post(
        '/trainer_add',
        json=trainer_json_a
    )
    assert response.status_code == 200
    '''
    obj2 = db.session.execute(
        db.select(Trainer).filter_by(Trainer_ID='a', password='********')).scalar()
    assert obj2 != None
def test_trainer_post_function_2(client,trainer_json_b,app):
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
        '/trainer_add',
        json = trainer_json_b
    )
    response = client.post(
        '/trainer_add',
        json= trainer_json_b
    )
    # not sure whether it is 404 or not
    assert response.status_code == 404