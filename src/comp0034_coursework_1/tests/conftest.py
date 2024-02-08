import os
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
import tempfile
db = SQLAlchemy()
ma = Marshmallow()
@pytest.fixture(scope='session')
def test_create_app(test_config=None):
    '''
    create test app and prevent the test_data contaminating the exsiting database
    :return: the test_app
    '''
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='F9cHlU7EQoj1JF5MRpZE1A',
        # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
    )
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + test_db_path
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    app.config.update({

        "TESTING": True,
        "SQLALCHEMY ECHO": True
    })
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    ma.init_app(app)

    from ..models import Trainer, Data, Player

    with app.app_context():
        db.create_all()
    yield app
    os.close(test_db_fd)  # Close the file descriptor
    os.unlink(test_db_path)  # Delete the temporary file

    # ensure the instance folder exists


@pytest.fixture(scope='session')

def client(app):
    '''

    define the test client

    '''
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
@pytest.fixture(scope='module')

def player_json_a():
    '''
    define the player_json_a,for the following tests
    '''
    player_json_1 = {
        'Player_ID' : 'arnold',
        'password' : '********',
        'Trainer_ID': 'a'
    }
@pytest.fixture(scope='module')
def player_json_b():
    '''
       define the player_json_b,for the following tests
    '''
    player_json_2 = {
        'Player_ID' : 'bill',
        'password' : '********',
        'Trainer_ID': 'b'
    }
@pytest.fixture(scope='module')
def player_json_c():
    '''
          define the player_json_c,for the following tests
    '''
    player_json_3 = {
        'Player_ID' : 'cat',
        'password' : '********',
        'Trainer_ID': 'a'
    }
    return player_json_3
@pytest.fixture(scope='module')
def trainer_json_a():
    '''
             define the trainer_json_a,for the following tests
    '''
    trainer_json_1= {
        'Trainer_ID': 'a',
        'password': '********'
    }
@pytest.fixture(scope='module')
def trainer_json_b():
    '''
               define the trainer_json_b,for the following tests
    '''
    train_json_2 = {
        'Trainer_ID': 'b',
        'password' : '********'
    }