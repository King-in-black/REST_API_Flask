import os
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .bp_get import get_bp
from .extension import db, ma
from .bp_post import post_bp
from .bp_delete import delete_bp
from .bp_put import put_bp
import pandas as pd
from .models import Data

current_file_path = os.path.realpath(__file__)
path = os.path.join(os.path.dirname(current_file_path), "..", "data", "data.csv")


def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(get_bp, url_prefix="/get")
    app.register_blueprint(post_bp, url_prefix="/post")
    app.register_blueprint(delete_bp, url_prefix="/delete")
    app.register_blueprint(put_bp, url_prefix="/put")
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY="F9cHlU7EQoj1JF5MRpZE1A",
        # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "IMU_data.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        # Put the following code inside the create_app function after the code to ensure the instance folder exists
        # This lis likely to be circa line 40.
    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(app)
    ma.init_app(app)
    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from .models import Trainer, Data, Player

    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        db.create_all()
        read_csv()
    return app
    # ensure the instance folder exists


def read_csv():
    """
    Adds data to the database through the csv file. A unique dataset_ID will be allocated to every csv file.
    Every data row's Data_ID will increase automatically. Read from csv. But overhere; only one csv as data file will be
    used.
    """
    # the csv locates in the data file
    if db.session.execute(db.select(Data)).first() == None:
        dataframe = pd.read_csv(path)
        dataframe.drop(dataframe.columns[0], axis=1, inplace=True)
        # drop the original index.
        print("Start adding IMU data to the database")
        # convert the timestamp to the format that database can understand
        dataframe["timestamp"] = pd.to_timedelta(
            "00:" + dataframe["timestamp"].astype(str)
        )
        # convert to total second number in float type
        dataframe["timestamp"] = dataframe["timestamp"].dt.total_seconds()
        ## check the maximum dataset_ID.
        max_dataset_id = db.session.execute(
            db.select(db.func.max(Data.Dataset_ID))
        ).scalar()
        if max_dataset_id is None:
            max_dataset_id = 0
        else:
            max_dataset_id += 1
        dataframe["Dataset_ID"] = max_dataset_id
        records = dataframe.to_dict(orient="records")
        # converts to the dictionary
        for datarow in records:
            data_row = Data(**datarow)  # Create data instance through the dictionary.
            db.session.add(data_row)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
