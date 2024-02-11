
from .extension import db,ma
from flask import Blueprint
put_bp = Blueprint('put', __name__)
from .schemas import Player_Schema,Trainer_Schema,Data_Schema
from flask import request,jsonify
from .models import Data,Player,Trainer

@put_bp.route('/player', methods=['PUT'])
def update_player():
    '''
    Allow user to update the password of the player
    '''
    data = request.get_json()
    new_record = Player_Schema().load(data)
    old_record = db.session.execute(db.select(Player).filter_by(Player_ID=new_record.Player_ID)).scalar()
    if not old_record:
        return jsonify({'message': 'Player not found'}), 404
    old_record.password = new_record.password
    db.session.commit()
    return jsonify({'message': 'Player password updated successfully'}), 201

@put_bp.route('/trainer', methods=['PUT'])
def update_trainer():
    '''
    Allow user to update the password of the trainer
    '''
    data = request.get_json()
    new_record = Trainer_Schema().load(data)
    old_record = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=new_record.Trainer_ID)).scalar()
    if not old_record:
        return jsonify({'message': 'Trainer not found'}), 404
    old_record.password = new_record.password
    db.session.commit()
    return jsonify({'message': 'Player password updated successfully'}), 201

@put_bp.route('/datarow/<code>', methods=['PUT'])
def update_Data(code):
    '''
        Allow user to update Data information according to the Data_ID
    '''
    data = request.get_json()
    new_record = Data_Schema().load(data)
    old_record = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar()
    if not old_record:
        return jsonify({'message': 'Player not found'}), 404
    old_record.password = new_record.password
    db.session.commit()
    return jsonify({'message': 'Player password updated successfully'}), 201