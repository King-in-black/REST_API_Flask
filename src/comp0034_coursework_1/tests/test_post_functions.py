from .. import models
from .. import schemas
# from father files import models and schemas
def test_player_post_function(client):
    '''

    :param client:
    :return:
    '''
    player_json= {

        'Player_ID' : 'arnold',
        'password' : '********',
        'Trainer_ID':'a'

    }
    response=client.post(
        '/player_add',
        json = player_json
    )

    assert response.status_code == 200
    obj = db.session.execute(db.select(Player).filter_by(Player_ID=player.Player_ID, password=player.password)).scalar()
    assert obj != None