from flask import Blueprint, jsonify

get_bp = Blueprint("get", __name__)
from .models import Player, Trainer, Data
from .schemas import Player_Schema, Trainer_Schema, Data_Schema
from .extension import db


@get_bp.errorhandler(409)
def resource_already_exist(e):
    return jsonify(error=str(e)), 409


@get_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@get_bp.errorhandler(500)
def Internet_error(e):
    return jsonify(error=str(e)), 500


@get_bp.errorhandler(400)
def Validation_error(e):
    return jsonify(error=str(e)), 400


@get_bp.get("/get_player/<code>")
def get_player(code):
    """
    The database will be requested to provide the information of the player with player ID
    return the json file of the player with certain ID.
    :param code: The ID  of the player
    :returns: the JSON format of the trainer with the certain ID
    """
    player = db.session.execute(
        db.select(Player).filter_by(Player_ID=code)
    ).scalar_one()
    result = Player_Schema().dump(player)
    return result


@get_bp.get("/get_trainer/<code>")
def get_trainer(code):
    """
    The database will be requested to provide the information of the trainer with certain trainer ID
    return the json file of the trainer with certain ID.
    :param code: The ID  of the trainer
    :returns: the JSON format of the trainer with the certain ID
    """

    trainer = db.session.execute(
        db.select(Trainer).filter_by(Trainer_ID=code)
    ).scalar_one()
    result = Trainer_Schema().dump(trainer)
    return result


@get_bp.get("/get_player_t/<code>")
def get_player_through_trainer_ID(code):
    """

    The database will be requested to provide the information of
    the player with certain trainer ID (foreign keys)
    return the json file of the player with certain trainer ID.
    :param code: The ID  of the trainer connecting with players
    :returns: the all JSONs  of the player with the certain ID

    """

    List = []
    a = db.session.execute(db.select(Player).filter_by(Trainer_ID=code))
    players = a.scalars().all()
    for i in players:
        result = Player_Schema().dump(i)
        List.append(result)
    return List


@get_bp.get("/Datarow_get/<code>")
def get_data(code):
    """Returns the json file of the data row with certain ID of data
    :param code: The ID  of the data row
    :returns: json format of certain data row
    """
    data = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar_one()
    # raise an error if multiple records are found
    result = Data_Schema().dump(data)
    return result


@get_bp.get("/Database_get/<code>")
def get_datarow_through_Database_ID(code):
    """
    Returns all the json files from same csv file with certain Dataset_ID.
    :param code: the dataset_ID of the dataset want to check
    :return: a list of the json files with same Dataset_ID
    """
    List = []
    obj = db.session.execute(db.select(Data).filter_by(Dataset_ID=code))
    data = obj.scalars().all()
    for i in data:
        result = Data_Schema().dump(i)
        List.append(result)
    if not List:
        return {"message": f"no datarow uploaded with the Dataset_ID{code}"}
    else:
        return List
