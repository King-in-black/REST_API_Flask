import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import csv
from pathlib import Path
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    app.config.from_mapping(
        SECRET_KEY='F9cHlU7EQoj1JF5MRpZE1A',
        # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'IMU_data.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
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

    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from router.models import Trainer, Data, Player
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        db.create_all()
        add_data_from_csv()
        from router import router
    return app
    # ensure the instance folder exists
def add_data_from_csv():
    """Adds data to the database if it does not already exist."""

    # Add import here and not at the top of the file to avoid circular import issues

    from comp0034_coursework_1.models import Data

    # If there are no Events, then add them
    first_data = db.session.execute(db.select(Data)).first()
    if not first_data:
        print("Start adding IMU data to the database")
        event_file = Path(__file__).parent.parent.joinpath("data", "data.csv")
        with open(event_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # row[0] is the first column, row[1] is the second column etc
                # For int data types, if there is no value, set to None rather than ''
                e = Data(
                          accX=row[1],
                          accY=row[2],
                          accZ=row[3],
                          gyroX=row[4],
                          gyroY=row[5],
                          gyroZ=row[6],
                          timestamp=row[7],
                          Activity =row[8],

                          )
                db.session.add(e)
            db.session.commit()

