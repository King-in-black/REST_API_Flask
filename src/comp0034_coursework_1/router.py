# Import the Flask class from the Flask library
# python -m src.comp0034_coursework_1.router
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    abort,
    Blueprint,
)
from . import create_app
from .extension import db
from .models import Trainer, Player, Data
from .schemas import Trainer_Schema, Data_Schema, Player_Schema
import jsonify
import pandas as pd
from flask import jsonify, request

# Create an instance of a Flask application
# import all the necessary functions to call the instance of schema and flasks
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
