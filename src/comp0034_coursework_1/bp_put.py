
from .extension import db,ma
from flask import Blueprint
put_bp = Blueprint('put', __name__)
from .schemas import Player_Schema,Trainer_Schema,Data_Schema
from flask import request,jsonify,abort
from .models import Data,Player,Trainer
@put_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404
@put_bp.route('/player', methods=['PUT'])
def update_player():
    '''
    Allow user to update the password of the player
    '''
    data = request.get_json()
    new_record = Player_Schema().load(data)
    old_record = db.session.execute(db.select(Player).filter_by(Player_ID=new_record.Player_ID)).scalar()
    if not old_record:
        abort(404, description="Player not found")
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
        return abort(404, description="Trainer not found")
    old_record.password = new_record.password
    db.session.commit()
    return jsonify({'message': 'Player password updated successfully'}), 201

@put_bp.route('/datarow/<code>', methods=['PUT'])
def update_Data(code):
    '''
        Allow user to update Data information according to the Data_ID
    '''
    new_record = request.get_json()
    old_record = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar()
    for key, value in new_record.items():
        # update the records
        setattr(old_record, key, value)
    if not old_record:
        return abort(404, description="Data_row not found")
    db.session.commit()
    return jsonify({'message': 'All of properties of data_row have changed'}), 201