from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extension import db


class Trainer(db.Model):
    """
    Add the trainer Model:
    Trainer_ID is the unique ID of trainer
    password is the password of the account
    """

    __tablename__ = "trainer"
    Trainer_ID: Mapped[str] = mapped_column(
        db.String(16), primary_key=True, nullable=False
    )
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    player: Mapped["Player"] = relationship("Player", back_populates="trainer")
    data: Mapped["data"] = relationship("Data", back_populates="trainer")


class Player(db.Model):
    """
    Add the player Model:
    Player_ID is the unique ID of player
    password is the password of the account
    """

    __tablename__ = "player"
    Player_ID: Mapped[str] = mapped_column(
        db.String(16), primary_key=True, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(db.String(32), unique=False, nullable=False)
    data: Mapped["data"] = relationship("Data", back_populates="player")
    Trainer_ID: Mapped[str] = mapped_column(
        ForeignKey("trainer.Trainer_ID"), nullable=True
    )
    trainer = relationship("Trainer", back_populates="player")


class Data(db.Model):
    """
    Add the Data Model from IMU　data with the Data_ID( ID for unique row)
    Dataset_ID is the unique ID for the csv
    Other properties are from csv
    Resultant_Acc,Resultant_Gyro,Average_Speed,Average_rotational_speed are contents predicted from
    machine learning model
    """

    __tablename__ = "data"
    Data_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Dataset_ID = db.Column(db.Integer, nullable=False)
    Player_ID: Mapped[str] = mapped_column(
        ForeignKey("player.Player_ID"), nullable=True
    )
    player = relationship("Player", back_populates="data")
    Trainer_ID: Mapped[str] = mapped_column(
        ForeignKey("trainer.Trainer_ID"), nullable=True
    )
    trainer = relationship("Trainer", back_populates="data")
    timestamp: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    accX: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    accY: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    accZ: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    gyroX: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    gyroY: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    gyroZ: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    Activity: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    Resultant_Acc: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    Resultant_Gyro: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    Average_Speed: Mapped[float] = mapped_column(db.Float(32), nullable=True)
    Average_rotational_speed: Mapped[float] = mapped_column(db.Float(32), nullable=True)
