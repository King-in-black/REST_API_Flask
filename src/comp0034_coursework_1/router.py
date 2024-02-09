# Import the Flask class from the Flask library
# python -m src.comp0034_coursework_1.router
from flask import Flask ,request ,redirect , url_for, render_template,flash ,abort
from .import create_app
from .import db
from .models import Trainer,Player,Data
from.schemas import Trainer_Schema,Data_Schema,Player_Schema
import jsonify
import pandas as pd
# Create an instance of a Flask application
#import all the necessary functions to call the instance of schema and flasks
app = create_app()
Trainer_Schema=Trainer_Schema()
Data_Schema=Data_Schema()
Player_Schema=Player_Schema()

@app.route('/homepage', methods=['GET', 'POST'])
# a homepage for the webapp
def homepage():
    '''
    when the user starts, they would like to starts from here to choose whether to login or register
    :return: the html which responsible for the homepage
    '''
    if request.method == 'POST':
        action = request.form.get('action')
        # according to the value of action, the page will redirect to another page.
        if action == 'login':
            # if the use types the button for login; they will jump to login page
            return redirect(url_for('login'))
        elif action == 'register':
            # or they will jump to register page
            return redirect(url_for('register'))
        else:
            return 'Invalid action', 400
    return render_template('button_homepage_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    allow people to register account in player identification or a trainer identification
    :return:
    if the user registers successfully, the user will jump into the login page;
    or they will return a 404 error
    '''
    if request.method == 'POST':
        player_id = request.form['Player_ID']
        trainer_id = request.form['Trainer_ID']
        password = request.form['password']
        role = request.form['role']

        if role == 'player':
            # the db will be asked to check whether there is a player ID
            existing_user = Player.query.filter_by(Player_ID=player_id).first()
            if existing_user:
            # if the player exists, the 404 error will return
                abort(404, description="Player already exists.")
            # or a Player instance will be asked to create in the database
            new_user = Player(Player_ID=player_id, password=password, Trainer_ID=trainer_id)
            db.session.add(new_user)
        elif role == 'trainer':
            # Check whether there is a player exists or not
            existing_user = Trainer.query.filter_by(Trainer_ID=trainer_id).first()
            if existing_user:
            # if the trainer exists, the 404 error will return
                abort(404, description="Trainer already exists.")
            # or a Trainer instance will be asked to create in the database
            new_user = Trainer(Trainer_ID=trainer_id, password=password)
            db.session.add(new_user)
        else:
            flash('Please select a valid role', 'error')
            return render_template('register.html')

        db.session.commit()  # submit the changes in the database
        # jump to login page if a user register successfully
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    '''
    the login page allows users to check records of existing players and trainers.
    if the password and ID are correct, they could access the following applications
    :returns: the following pages have not completed.
    '''
    if request.method == 'POST':
        # extract the information of the players or the trainers
        role = request.form['role']
        user_id = request.form.get('user_id')
        password = request.form['password']

        if role == 'player':
            # if the user is player, the database will be asked for certain records of the player
            # if the password and the ID of the form requested match with records in the database
            # login page passed
            user = Player.query.filter_by(Player_ID=user_id, password=password).scalarone()
            if user:
                # when the player login successfully, the following steps will be inplemented
                flash('Player login successful!', 'success')
                return redirect(url_for('player_dashboard'))  # incomplete player page for prediction the result
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Player ID or password', 'error')

        elif role == 'trainer':
            # when the trainer login successfully, the following steps will be inplemented
            user = Trainer.query.filter_by(Trainer_ID=user_id, password=password).scalarone()
            if user:
                # when the trainer login successfully, the following steps will be inplemented
                flash('Trainer login successful!', 'success')
                return redirect(url_for('trainer_dashboard'))  # incomplete trainer page for upload the results
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Trainer ID or password', 'error')

    return render_template('login.html')


@app.get('/trainer/<code>')
def get_trainer(code):
    """
    The database will be requested to provide the information of the trainer with certain trainer ID
    return the json file of the trainer with certain ID.
    :param code: The ID  of the trainer
    :returns: the JSON format of the trainer with the certain ID
    """

    trainer = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=code)).scalar_one()
    result = Trainer_Schema.dump(trainer)
    return result

@app.get('/player/<code>')
def get_player(code):
    """

    The database will be requested to provide the information of the player with certain player ID
    return the json file of the player with certain ID.
    :param code: The ID  of the player
    :returns: the JSON format of the player with the certain ID

    """
    player = db.session.execute(db.select(Player).filter_by(Player_ID=code)).scalar_one()
    result = Player_Schema.dump(player)
    return result

@app.get('/player_t/<code>')
def get_player_through_trainer_ID(code):
    """

    The database will be requested to provide the information of the player with certain trainer ID (foreign keys)
    return the json file of the player with certain trainer ID.
    :param code: The ID  of the trainer connecting with players
    :returns: the all JSONs  of the player with the certain ID

    """

    List=[]
    a = db.session.execute(db.select(Player).filter_by(Trainer_ID=code))
    players = a.scalars().all()
    for i in players:
        result = Player_Schema.dump(i)
        List.append(result)
    return List

@app.post('/player_add')
def create_player():
    '''

    The database will be requested to add the information of the player(ID and password)
     with the json file
    :return: the message of the player wi


    th certain player_ID is added successfully.

    '''
    player_json=request.get_json()
    player= Player_Schema.load(player_json)
    db.session.add(player)
    db.session.commit()
    return {"message":f"Player added with the player_ID={player.Player_ID}"}

@app.post('/trainer_add')
def create_trainer():
    '''

        The database will be requested to add the information of the trainer(ID and password)
         with the json file
        :return: the message of the trainer with certain trainer_ID is added successfully.

    '''
    trainer_json=request.get_json()
    trainer= Trainer_Schema.load(trainer_json)
    db.session.add(trainer)
    db.session.commit()
    return {"message":f"Trainer added with the trainer_ID={trainer.Trainer_ID}"}


@app.delete('/delete_player')
def delete_player():
    '''

     The database will be requested to delete the information of the player(ID and password) with the json file.
     After getting the request, the database will check whether the record fits. Then the player will  delete if correct
     password and player ID has been input.

    '''
    player_json = request.get_json()
    player = Player_Schema.load(player_json)
    del_obj = db.session.execute(db.select(Player).filter_by(Player_ID=player.Player_ID, password=player.password)).scalar_one()
    # delete the certain record
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message': f'Record of Player  {player.Player_ID} deleted successfully'}
    else:
        return {'error': 'Record of Player not found'}

@app.delete('/delete_trainer')
def delete_trainer():
    '''

    The database will be requested to delete the information of the trainer(ID and password) with the json file.
    After getting the request, the database will check whether the record fits. Then the trainer will  delete if correct
    password and trainer ID has been matched

    '''
    trainer_json = request.get_json()
    trainer = Trainer_Schema.load(trainer_json)
    del_obj = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=trainer.Trainer_ID, password=trainer.password)).scalar_one()
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message':'Record of Trainer deleted  successfully'}
    else:
        return {'error': 'Record of Trainer not found'}


@app.route('/Database_add',methods=['GET', 'POST'])
def add_data_from_csv():
    """
    Adds data to the database through the csv file. A unique dataset_ID will be allocated to every csv file.
    Every data row's Data_ID will increase automatically. Read from

    """
    # the csv locates in the data file
    dataframe = pd.read_csv("E:\\Programming_Assignments\\comp0034-cw1i-King-in-black\\src\\data\\data.csv")
    dataframe = dataframe.drop(dataframe.columns.values[0])
    # drop the original index.
    print("Start adding IMU data to the database")
    # convert the timestamp to the format that database can understand
    dataframe['timestamp'] = pd.to_timedelta('00:' + dataframe['timestamp'].astype(str))
    # convert to total second number in float type
    dataframe['timestamp'] = dataframe['timestamp'].dt.total_seconds()
    # check the maximum dataset_ID.
    max_dataset_id = db.session.execute(db.select(db.func.max(Data.Dataset_ID))).scalar()
    if max_dataset_id is None:
        max_dataset_id = 0
    else:
        max_dataset_id += 1
    dataframe['Dataset_ID'] = max_dataset_id
    records = dataframe.to_dict(orient='records')
    # converts to the dictionary
    for datarow in records:
        data_row = Data(**datarow)  # Create data instance through the dictionary.
        db.session.add(data_row)
    db.session.commit()
    return {"message":f"Dataset added with the Dataset_ID={max_dataset_id}"}

@app.route('/Datarow_add',methods=['GET', 'POST'])
def create_Datarow():
    '''
    add a data row with a json file with certain content.
    '''
    data_json = request.get_json()
    data = Data_Schema.load(data_json)
    db.session.add(data)
    db.session.commit()
    return {"message":f"Data added with the Data_ID={data.Data_ID} and with the Data_base={data.Dataset_ID}"}

@app.get('/Datarow_get/<code>')
def get_data(code):
    """Returns the json file of the data row with certain ID of data
    :param code: The ID  of the data row
    :returns: json format of certain data row
    """
    data = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar_one()
    # raise an error if multiple records are found
    result = Data_Schema.dump(data)
    return result
@app.get('/Database_get/<code>')
def get_datarow_through_Database_ID(code):
    '''
    Returns all the json files from same csv file with certain Dataset_ID.
    :param code: the dataset_ID of the dataset want to check
    :return: a list of the json files with same Dataset_ID
    '''
    List=[]
    obj = db.session.execute(db.select(Data).filter_by(Dataset_ID=code))
    data = obj.scalars().all()
    for i in data:
        result = Data_Schema.dump(i)
        List.append(result)
    if not List:
        return {'message':f'no datarow uploaded with the Dataset_ID{code}'}
    else:
        return List

@app.delete('/delete_datarow/<code>')
def delete_Datarow(code):
    '''
    The database will be requested to delete the information of the Data row with the data_ID.
    After getting the request, the database will check whether the record fits. Then the data row will  delete if there is
    the Data_ID
    :param code: the data_ID that user want to delete
    '''
    del_obj = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar_one()
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message': 'Record of Data_row deleted successfully'}
    else:
        return {'error': 'Record of Data_row not found'}


@app.delete('/delete_database/<code>')
def delete_Database(code):
    '''
        The database will be requested to delete the information of the Dataset with the dataset_ID.
        After getting the request, the database will check whether the record fits. Then the dataset will delete if there is
        the matched dataset_ID
        :param code: the dataset_ID that user want to delete
    '''
    a = db.session.execute(db.select(Data).filter_by(Dataset_ID=code))
    data = a.scalars().all()
    if data:
        for i in data:
            db.session.delete(i)
        db.session.commit()
        return {'message': 'Record of Database deleted  successfully'}
    else:
        return {'error': 'Record of Data_base not found'}

@app.route('/datarow/<code1>/player/<code2>',methods=["GET","POST"])
def row_relationship_addition_player(code1,code2):
    '''
    The database add relationship between datarow and player
    :param code1: the data_ID of the data row
    :param code2: the player_ID of player account
    :return:
    '''
    data_row = db.session.execute(db.select(Data).filter_by(Data_ID=code1)).scalar_one()
    player = db.session.execute(db.select(Player).filter_by(Player_ID=code2)).scalar_one()
    if not data_row.player:
       data_row.player = player
       db.session.commit()
       return {'message': f'Records between data_row {data_row.Data_ID} and player{player.Player_ID} are connected'}
    else:
       return{'error':f'The relationship has already exist between data_row {data_row.Data_ID} and player{data_row.Player_ID}'}

@app.route('/datarow/<code1>/trainer/<code2>',methods=["GET","POST"])
def row_relationship_addition_trainer(code1,code2):
    '''

    The database add relationship between datarow and trainer
    :param code1: the data_ID of the data row
    :param code2: the Trainer_ID of trainer account
    :return: messages of success

    '''
    data_row = db.session.execute(db.select(Data).filter_by(Data_ID=code1)).scalar_one()
    trainer = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=code2)).scalar_one()
    if not data_row.trainer:
       data_row.trainer = trainer
       db.session.commit()
       return {'message': f'Records between data_row {data_row.Data_ID} and trainer{trainer.Trainer_ID} has already been connected'}
    else:
       return{'error':f'The relationship has already exist between data_row {data_row.Data_ID} and trainer{data_row.Trainer_ID}'}


if __name__ == '__main__':
    app.run(debug=True)