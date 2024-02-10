import os
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .bp_get import get_bp
from.extension import db,ma
from .bp_post import post_bp

def create_app(test_config=None):
    # create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(get_bp, url_prefix='/get')
    app.register_blueprint(post_bp, url_prefix='/post')
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
    ma.init_app(app)
    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from .models import Trainer, Data, Player
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        db.create_all()
    return app
    # ensure the instance folder exists

if __name__ == '__main__':
    app= create_app()


