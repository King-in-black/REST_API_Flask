from flask import Blueprint
post_bp = Blueprint('post', __name__)
from .schemas import Player_Schema,Trainer_Schema,Data_Schema
from .extension import db
from flask import request,jsonify


@post_bp.route('/player_add',methods=['GET', 'POST'])
def create_player():
    player_json = request.get_json()
    player = Player_Schema.load(player_json)
    db.session.add(player)
    db.session.commit()
    return jsonify({"message": f"Player added with the player_ID={player.Player_ID}"}), 201

@post_bp.route('/trainer_add',methods=['GET', 'POST'])
def create_trainer():
    '''

        The database will be requested to add the information of the trainer(ID and password)
         with the json file
        :return: the message of the trainer with certain trainer_ID is added successfully.

    '''
    trainer_json=request.get_json()
    print(trainer_json)
    trainer= Trainer_Schema.load(trainer_json)
    print(trainer)
    db.session.add(trainer)
    db.session.commit()
    return {"message":f"Trainer added with the trainer_ID={trainer.Trainer_ID}"}

@post_bp.route('/Datarow_add',methods=['GET', 'POST'])
def create_Datarow():
    '''
    add a data row with a json file with certain content.
    '''
    data_json = request.get_json()
    data = Data_Schema.load(data_json)
    db.session.add(data)
    db.session.commit()
    return {"message":f"Data added with the Data_ID={data.Data_ID} and with the Data_base={data.Dataset_ID}"}
