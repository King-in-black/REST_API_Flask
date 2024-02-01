
# Adapted from https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models
from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db
from datetime import  datetime
class Trainer(db.Model):
    __tablename__ ='trainer'
    Trainer_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,nullable=False)
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    Player_ID: Mapped[str] = mapped_column(ForeignKey("player.Player_ID"))
    player = relationship('Player',back_populates="trainer",foreign_keys=Player_ID)
    Data_ID: Mapped[str] = mapped_column(ForeignKey("data.Data_ID"))
    data = relationship('Data',back_populates="trainer",foreign_keys=Data_ID)
# This uses the latest syntax for SQLAlchemy, older tutorials will show different syntax
# SQLAlchemy provide an __init__ method for each model, so you do not need to declare this in your code
class Player(db.Model):
    __tablename__ = "player"
    Player_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,unique=True,nullable=False)
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    Data_ID: Mapped[str] = mapped_column(ForeignKey("data.Data_ID"))
    data = relationship('Data', back_populates="player", foreign_keys=Data_ID)
    Trainer_ID: Mapped[str] = mapped_column(ForeignKey("trainer.Trainer_ID"))
    trainer = relationship('Trainer', back_populates="player",foreign_keys=Trainer_ID)
    # one-to-many relationship with Event, the relationship in Event is called 'region'
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many

class Data(db.Model):
    __tablename__ = "data"
    Data_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,unique=True,nullable=False)
    Player_ID: Mapped[str] = mapped_column(ForeignKey("player.Player_ID"))
    player = relationship('Player', back_populates="data",foreign_keys='Player_ID')
    Trainer_ID: Mapped[str] = mapped_column(ForeignKey("trainer.Trainer_ID"))
    trainer = relationship('Trainer', back_populates="data",foreign_keys='Trainer_ID')
    Timestamp: Mapped[datetime] = mapped_column(db.DateTime,nullable=True)
    accX: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    accY: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    accZ: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    gyroX: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    gyroY: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    gyroZ: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    Activity: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    Resultant_Acc : Mapped[float] = mapped_column(db.Float(32),nullable=True)
    Resultant_Gyro : Mapped[float] = mapped_column(db.Float(32),nullable=True)
    Average_Speed: Mapped[float] = mapped_column(db.Float(32),nullable=True)
    Average_rotational_speed:Mapped[float] = mapped_column(db.Float(32),nullable=True)


