import pytest
from .. import create_app
# import create_app()
@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
                       "TESTING": True,
                       "SQLALCHEMY ECHO": True
    })
    yield app

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
@pytest.fixture(scope='module')
def define_a_player_json_a():
    player_json_1 = {
        'Player_ID' : 'arnold',
        'password' : '********',
        'Trainer_ID': 'a'
    }
@pytest.fixture(scope='module')
def define_a_player_json_b():
    player_json_2 = {
        'Player_ID' : 'bill',
        'password' : '********',
        'Trainer_ID': 'b'
    }
@pytest.fixture(scope='module')
def define_a_player_json_c():
    player_json_3 = {
        'Player_ID' : 'cat',
        'password' : '********',
        'Trainer_ID': 'a'
    }
@pytest.fixture(scope='module')
def define_a_trainer_json_a():
    trainer_json_1= {
        'Trainer_ID': 'a',
        'password': '********'
    }
@pytest.fixture(scope='module')
def define_a_trainer_json_b():
    train_json_2 = {
        'Trainer_ID': 'b',
        'password' : '********'
    }