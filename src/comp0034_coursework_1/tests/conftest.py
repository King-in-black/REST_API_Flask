import os
from flask import Flask
import pytest
import tempfile
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from.. import create_app
from .. import db
from .. import ma
@pytest.fixture(scope='module')
def app():
    app=create_app()
    app.config.update({'TESTING':True,
                       })
    yield app
@pytest.fixture(scope='module')
def client(app):
    '''

    define the test client

    '''
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
@pytest.fixture(scope='session')

def player_json_a():
    '''
    define the player_json_a,for the following tests
    '''
    player_json_1 = {
        'Player_ID' : 'arnold',
        'password' : '********',
        'Trainer_ID': 'a'
    }
    return player_json_1
@pytest.fixture(scope='session')
def player_json_b():
    '''
       define the player_json_b,for the following tests
    '''
    player_json_2 = {
        'Player_ID' : 'bill',
        'password' : '********',
        'Trainer_ID': 'b'
    }
    return player_json_2
@pytest.fixture(scope='session')
def player_json_c():
    '''
          define the player_json_c,for the following tests
    '''
    player_json_3 = {
        'Player_ID' : 'cat',
        'password' : '********',
        'Trainer_ID' :'a'
    }
    return player_json_3
@pytest.fixture(scope='session')
def trainer_json_a():
    '''
             define the trainer_json_a,for the following tests
    '''
    trainer_json_1= {
        'Trainer_ID': 'a',
        'password': '********'
    }
    return trainer_json_1
@pytest.fixture(scope='session')
def trainer_json_b():
    '''
               define the trainer_json_b,for the following tests
    '''
    trainer_json_2 = {
        'Trainer_ID': 'b',
        'password' : '********'
    }
    return trainer_json_2
@pytest.fixture(scope='session')
def data_row_json():
    data_json= { "Dataset_ID" : "1",
                 "Player_ID" : "arnold",
                 'Trainer_ID':'a',
                  "timestamp":1,
                   "accX" :1,
                   "accY" :1,
                   "accZ":1,
                    "gyroX":1,
                    "gyroY":1,
                     "gyroZ":1,
                    "Activity":1,
                    "Resultant_Acc":1,
                     "Resultant_Gyro":1,
                 "Average_Speed":1,
                 'Average_rotational_speed':1
                 }
    return data_json