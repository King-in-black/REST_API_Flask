from flask import Blueprint,request,jsonify
delete_bp = Blueprint('delete', __name__)
from .models import Player,Trainer,Data
from .schemas import Player_Schema,Trainer_Schema,Data_Schema
from .extension import db
@delete_bp.errorhandler(409)
def resource_already_exist(e):
    return jsonify(error=str(e)), 409
@delete_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404
@delete_bp.errorhandler(500)
def Internet_error(e):
    return jsonify(error=str(e)), 500
@delete_bp.errorhandler(400)
def Validation_error(e):
    return jsonify(error=str(e)), 400
@delete_bp.route('/delete_player', methods=['DELETE'])
def delete_player():
    '''

     The database will be requested to delete the information of the player(ID and password) with the json file.
     After getting the request, the database will check whether the record fits. Then the player will  delete if correct
     password and player ID has been input.

    '''
    player_json = request.get_json()
    player = Player_Schema().load(player_json)
    del_obj = db.session.execute(db.select(Player).filter_by(Player_ID=player.Player_ID, password=player.password)).scalar()
    # delete the certain record
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return jsonify({'message': f'Record of Player  {player.Player_ID} deleted successfully'}),201
    else:
        return jsonify({'error': 'Record of Player not found'}), 409

@delete_bp.route('/delete_trainer', methods=['DELETE'])
def delete_trainer():
    '''

    The database will be requested to delete the information of the trainer(ID and password) with the json file.
    After getting the request, the database will check whether the record fits. Then the trainer will  delete if correct
    password and trainer ID has been matched

    '''
    trainer_json = request.get_json()
    trainer = Trainer_Schema().load(trainer_json)
    del_obj = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=trainer.Trainer_ID, password=trainer.password)).scalar()
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return jsonify({'message': 'Record of Trainer deleted  successfully'}),201
    else:
        return jsonify({'error': 'Record of Trainer not found'}),409

@delete_bp.route('/delete_datarow/<code>', methods=['DELETE'])
def delete_Datarow(code):
    '''
    The database will be requested to delete the information of the Data row with the data_ID.
    After getting the request, the database will check whether the record fits. Then the data row will  delete if there is
    the Data_ID
    :param code: the data_ID that user want to delete
    '''
    del_obj = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar()
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return jsonify({'message': 'Record of Data_row deleted successfully'}),201
    else:
        return jsonify({'error': 'Record of Data_row not found'}),409