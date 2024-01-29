
# Adapted from https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models
from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Router import db
from datetime import  datetime
class Trainer(db.Model):
    __tablename__ ='trainer'
    Trainer_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,nullable=False)
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    Player_ID: Mapped[str] = mapped_column(ForeignKey("player.Player_ID"))
    player = relationship('Player',back_populates="trainer")
    Data_ID: Mapped[str] = mapped_column(ForeignKey("data.Data_ID"))
    data = relationship('Data',back_populates="trainer")
# This uses the latest syntax for SQLAlchemy, older tutorials will show different syntax
# SQLAlchemy provide an __init__ method for each model, so you do not need to declare this in your code
class Player(db.Model):
    __tablename__ = "player"
    Player_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,unique=True,nullable=False)
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    Data_ID: Mapped[str] = mapped_column(ForeignKey("data.Data_ID"))
    data = relationship('Data', back_populates="player")
    Trainer_ID: Mapped[str] = mapped_column(ForeignKey("trainer.Trainer_ID"))
    trainer = relationship('Trainer', back_populates="player")
    # one-to-many relationship with Event, the relationship in Event is called 'region'
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many

class Data(db.Model):
    __tablename__ = "data"
    Data_ID: Mapped[str] = mapped_column(db.String(16), primary_key=True,unique=True,nullable=False)
    Player_ID: Mapped[str] = mapped_column(ForeignKey("player.Player_ID"))
    player = relationship('Player', back_populates="data")
    Trainer_ID: Mapped[str] = mapped_column(ForeignKey("trainer.Trainer_ID"))
    trainer = relationship('Trainer', back_populates="data")
    Timestamp: Mapped[datetime] = mapped_column(db.Datetime,nullable=True)
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
    Total_displacement:Mapped[float] = mapped_column(db.Float(32),nullable=True)
    Total_time : Mapped[datetime] = mapped_column(db.Datetime,nullable=True)


    def __init__(self, email: str, password: str):
        """
        Create a new User object using hashing the plain text password.
        :type password_string: str
        :type email: str
        :returns None
        """
        self.email = email
        self.password = password