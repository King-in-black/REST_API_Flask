from .extension import ma
from .extension import db
from .models import Trainer, Player, Data


class Data_Schema(ma.SQLAlchemySchema):
    class Meta:
        model = Data
        sqla_session = db.session
        load_instance = True
        include_relationships = True

    Data_ID = ma.auto_field()
    Dataset_ID = ma.auto_field()
    Player_ID = ma.auto_field()
    Trainer_ID = ma.auto_field()
    timestamp = ma.auto_field()
    accX = ma.auto_field()
    accY = ma.auto_field()
    accZ = ma.auto_field()
    gyroX = ma.auto_field()
    gyroY = ma.auto_field()
    gyroZ = ma.auto_field()
    Activity = ma.auto_field()
    Resultant_Acc = ma.auto_field()
    Resultant_Gyro = ma.auto_field()
    Average_Speed = ma.auto_field()
    Average_rotational_speed = ma.auto_field()


class Trainer_Schema(ma.SQLAlchemySchema):
    class Meta:
        model = Trainer
        sqla_session = db.session
        load_instance = True
        include_relationships = True

    Trainer_ID = ma.auto_field()
    password = ma.auto_field()


class Player_Schema(ma.SQLAlchemySchema):
    class Meta:
        model = Player
        sqla_session = db.session
        load_instance = True
        include_relationships = True

    Player_ID = ma.auto_field()
    password = ma.auto_field()
    Trainer_ID = ma.auto_field()
