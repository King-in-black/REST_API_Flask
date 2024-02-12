from flask import Blueprint

post_bp = Blueprint("post", __name__)
from .schemas import Player_Schema, Trainer_Schema, Data_Schema
from .extension import db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from .models import Data, Player, Trainer


@post_bp.errorhandler(409)
def resource_already_exist(e):
    return jsonify(error=str(e)), 409


@post_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@post_bp.errorhandler(500)
def Internet_error(e):
    return jsonify(error=str(e)), 500


@post_bp.errorhandler(400)
def Validation_error(e):
    return jsonify(error=str(e)), 400


@post_bp.route("/player_add", methods=["POST"])
def create_player():
    """

    The database will be requested to add the information of the player(ID and password)
     with the json file
    :return: the message of the trainer with certain player_ID is added successfully.

    """
    try:
        player_json = request.get_json()
        player = Player_Schema().load(player_json)
        if (
            db.session.execute(
                db.select(Player).filter_by(Player_ID=player.Player_ID)
            ).scalar()
        ) != None:
            return jsonify({"error": "User with this ID already exists"}), 409
        db.session.add(player)
        db.session.commit()
        return (
            jsonify({"message": f"Player added with the player_ID={player.Player_ID}"}),
            201,
        )
    except ValidationError as e:
        db.session.rollback()
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@post_bp.route("/trainer_add", methods=["GET", "POST"])
def create_trainer():
    """

    The database will be requested to add the information of the trainer(ID and password)
     with the json file
    :return: the message of the trainer with certain trainer_ID is added successfully.

    """
    try:
        trainer_json = request.get_json()
        trainer = Trainer_Schema().load(trainer_json)
        if (
            db.session.execute(
                db.select(Trainer).filter_by(Trainer_ID=trainer.Trainer_ID)
            ).scalar()
        ) != None:
            return jsonify({"error": "User with this ID already exists"}), 409
        db.session.add(trainer)
        db.session.commit()
        return (
            jsonify(
                {"message": f"Trainer added with the trainer_ID={trainer.Trainer_ID}"}
            ),
            201,
        )
    except ValidationError as e:
        db.session.rollback()
        return jsonify(e.messages), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this ID already exists"}), 409
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@post_bp.route("/Datarow_add", methods=["GET", "POST"])
def create_Datarow():
    """
    add a data row from a json file with certain content.
    """
    try:
        data_json = request.get_json()
        data = Data_Schema().load(data_json)
        if (
            db.session.execute(db.select(Data).filter_by(Data_ID=data.Data_ID)).scalar()
        ) != None:
            return jsonify({"error": "User with this ID already exists"}), 409
        db.session.add(data)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": f"Data added with the Data_ID={data.Data_ID} and with the Data_base={data.Dataset_ID}"
                }
            ),
            201,
        )
    except ValidationError as e:
        db.session.rollback()
        return jsonify(e.messages), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this ID already exists"}), 409
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
