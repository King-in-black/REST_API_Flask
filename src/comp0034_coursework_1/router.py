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
            user = Player.query.filter_by(Player_ID=user_id, password=password).first()
            if user:
                # when the player login successfully, the following steps will be inplemented
                flash('Player login successful!', 'success')
                return redirect(url_for('player_dashboard'))  # incomplete player page for prediction the result
            else:
                # when there is a failure, the following styles will be implemented
                flash('Invalid Player ID or password', 'error')

        elif role == 'trainer':
            # when the trainer login successfully, the following steps will be inplemented
            user = Trainer.query.filter_by(Trainer_ID=user_id, password=password).first()
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
    :return: the message of the player with certain player_ID is added successfully.

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
    :return:
    '''
    player_json = request.get_json()
    player = Player_Schema.load(player_json)
    del_obj = db.session.execute(db.select(Player).filter_by(Player_ID=player.Player_ID)).scalar_one()
    # 查找并删除指定的记录
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message': 'Record of Player deleted successfully'}
    else:
        return {'error': 'Record of Player not found'}

@app.delete('/delete_trainer')
def delete_trainer():
    '''
    The database will be requested to delete the information of the player(ID and password)
    with the json file of the certain trainer
        :return: the message of the player with certain trainer_ID is added successfully.
    '''
    trainer_json = request.get_json()
    trainer = Trainer_Schema.load(trainer_json)
    del_obj = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=trainer.Trainer_ID)).scalar_one()
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message':'Record of Trainer deleted  successfully'}
    else:
        return {'error': 'Record of Trainer not found'}


@app.route('/Database_add',methods=['GET', 'POST'])
def add_data_from_csv():
    """
    Adds data to the database if it does not already exist.

    """
    dataframe = pd.read_csv("E:\\Programming_Assignments\\comp0034-cw1i-King-in-black\\src\\data\\data.csv")
    dataframe.columns.values[0] = 'Data_ID'
    dataframe = dataframe.drop(columns='Data_ID')
    print("Start adding IMU data to the database")
    # 先将timestamp列转换为timedelta类型
    dataframe['timestamp'] = pd.to_timedelta('00:' + dataframe['timestamp'].astype(str))
    # 然后将timedelta转换为总秒数的浮点数
    dataframe['timestamp'] = dataframe['timestamp'].dt.total_seconds()
    max_dataset_id =db.session.execute(db.select(db.func.max(Data.Dataset_ID))).scalar()
    if max_dataset_id is None:
        max_dataset_id = 0
    else:
        max_dataset_id += 1
    dataframe['Dataset_ID'] = max_dataset_id
    records = dataframe.to_dict(orient='records')
    # converts to the dictionary
    for datarow in records:
        data_row = Data(**datarow)  # 使用字典解包创建Data实例
        db.session.add(data_row)
    db.session.commit()
    return {"message":f"Dataset added with the Dataset_ID={max_dataset_id}"}

@app.route('/Datarow_add',methods=['GET', 'POST'])
def create_Datarow():
    data_json=request.get_json()
    data= Data_Schema.load(data_json)
    db.session.add(data)
    db.session.commit()
    return {"message":f"Data added with the Data_ID={data.Data_ID} and with the Data_base={data.Dataset_ID}"}

@app.get('/Datarow_get/<code>')
def get_data(code):
    """Returns the json file of the player with certain ID
    :param code: The ID  of the player
    :param type code: str
    :returns: JSON
    """
    # Query structure shown at https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#select
    data = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar_one()
    # Dump the data using the Marshmallow region schema; .dump() returns JSON
    result = Data_Schema.dump(data)
    # Return the data in the HTTP response
    return result
@app.get('/Database_get/<code>')
def get_datarow_through_Database_ID(code):
    '''

    :param code:
    :return:
    '''
    List=[]
    obj = db.session.execute(db.select(Data).filter_by(Dataset_ID=code))
    data = obj.scalars().all()
    for i in data:
        result = Data_Schema.dump(i)
        List.append(result)
    return List

@app.delete('/delete_datarow/<code>')
def delete_Datarow(code):
    del_obj = db.session.execute(db.select(Data).filter_by(Data_ID=code)).scalar_one()
    # 查找并删除指定的记录
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return {'message': 'Record of Data_row deleted successfully'}
    else:
        return {'error': 'Record of Data_row not found'}

@app.delete('/delete_database/<code>')
def delete_Database(code):
    a = db.session.execute(db.select(Data).filter_by(Dataset_ID=code))
    data = a.scalars().all()
    if data:
        for i in data:
            db.session.delete(i)
        db.session.commit()
        return {'message': 'Record of Database deleted  successfully'}
    else:
        return {'error': 'Record of Database not found'}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)