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
# The first argument is the name of the application’s module or package. __name__ is a convenient shortcut.
# This is needed so that Flask knows where to look for resources such as templates and static files.
# Add a route for the 'home' page
# use the route() decorator to tell Flask what URL should trigger our function.
app = create_app()
Trainer_Schema=Trainer_Schema()
Data_Schema=Data_Schema()
Player_Schema=Player_Schema()
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        action = request.form.get('action')
        # according to the value of action, the page will redirect to another page.
        if action == 'login':
            return redirect(url_for('login'))
        elif action == 'register':
            return redirect(url_for('register'))
        else:
            return 'Invalid action', 400
    return render_template('button_homepage_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        player_id = request.form['Player_ID']
        trainer_id = request.form['Trainer_ID']
        password = request.form['password']
        role = request.form['role']

        if role == 'player':
            # 检查Player是否已存在
            existing_user = Player.query.filter_by(Player_ID=player_id).first()
            if existing_user:
                # 如果用户已存在，返回404或其他合适的错误处理
                abort(404, description="Player already exists.")
            # 创建Player实例并写入数据库
            new_user = Player(Player_ID=player_id, password=password, Trainer_ID=trainer_id)
            db.session.add(new_user)
        elif role == 'trainer':
            # 检查Trainer是否已存在
            existing_user = Trainer.query.filter_by(Trainer_ID=trainer_id).first()
            if existing_user:
                # 如果用户已存在，返回404或其他合适的错误处理
                abort(404, description="Trainer already exists.")
            # 创建Trainer实例并写入数据库
            new_user = Trainer(Trainer_ID=trainer_id, password=password)
            db.session.add(new_user)
        else:
            flash('Please select a valid role', 'error')
            return render_template('register.html')

        db.session.commit()  # 提交数据库更改
        # 成功注册后的逻辑
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 提取表单数据
        role = request.form['role']
        user_id = request.form.get('user_id')
        password = request.form['password']

        if role == 'player':
            # 如果是玩家，查询Player表
            user = Player.query.filter_by(Player_ID=user_id, password=password).first()
            if user:
                # 登录成功逻辑
                flash('Player login successful!', 'success')
                return redirect(url_for('player_dashboard'))  # 假设有一个玩家仪表板视图
            else:
                # 登录失败逻辑
                flash('Invalid Player ID or password', 'error')

        elif role == 'trainer':
            # 如果是教练，查询Trainer表
            user = Trainer.query.filter_by(Trainer_ID=user_id, password=password).first()
            if user:
                # 登录成功逻辑
                flash('Trainer login successful!', 'success')
                return redirect(url_for('trainer_dashboard'))  # 假设有一个教练仪表板视图
            else:
                # 登录失败逻辑
                flash('Invalid Trainer ID or password', 'error')

    return render_template('login.html')


@app.get('/trainer/<code>')
def get_trainer(code):
    """Returns the json file of the trainer with certain ID

    :param code: The ID  of the trainer
    :param type code: str
    :returns: JSON
    """
    # Query structure shown at https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#select
    trainer = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=code)).scalar_one()
    # Dump the data using the Marshmallow region schema; .dump() returns JSON
    result = Trainer_Schema.dump(trainer)
    return result

@app.get('/player/<code>')
def get_player(code):
    """Returns the json file of the player with certain ID
    :param code: The ID  of the player
    :param type code: str
    :returns: JSON
    """
    # Query structure shown at https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#select
    player = db.session.execute(db.select(Player).filter_by(Player_ID=code)).scalar_one()
    # Dump the data using the Marshmallow region schema; .dump() returns JSON
    result = Player_Schema.dump(player)
    # Return the data in the HTTP response
    return result

@app.get('/player_t/<code>')
def get_player_through_trainer_ID(code):
    """Returns the json file of the players with certain trainer
    :param code: The ID  of the trainer responsible for the player
    :param type code: str
    :returns: JSON
    """
    # Query structure shown at https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/#select
    List=[]
    #player = db.session.execute(db.select(Player).filter_by(Trainer_ID=code)).all()
    a = db.session.execute(db.select(Player).filter_by(Trainer_ID=code))
    players = a.scalars().all()
    for i in players:
        result = Player_Schema.dump(i)
        List.append(result)
    return List

@app.post('/player_add')
def create_player():
    player_json=request.get_json()
    player= Player_Schema.load(player_json)
    db.session.add(player)
    db.session.commit()
    return {"message":f"Player added with the player_ID={player.Player_ID}"}

@app.post('/trainer_add')
def create_trainer():
    trainer_json=request.get_json()
    trainer= Trainer_Schema.load(trainer_json)
    db.session.add(trainer)
    db.session.commit()
    return {"message":f"Trainer added with the trainer_ID={trainer.Trainer_ID}"}


@app.delete('/delete_trainer')
def delete_trainer():
    trainer_json = request.get_json()
    trainer = Trainer_Schema.load(trainer_json)
    del_obj = db.session.execute(db.select(Trainer).filter_by(Trainer_ID=trainer.Trainer_ID)).scalar_one()
    # 查找并删除指定的记录
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return jsonify({'message': 'Record of Trainer deleted  successfully'}), 200
    else:
        return jsonify({'error': 'Record of Trainer not found'}), 404

@app.delete('/delete_player')
def delete_player():
    player_json = request.get_json()
    player = Player_Schema.load(player_json)
    del_obj = db.session.execute(db.select(Player).filter_by(Player_ID=player.Player_ID)).scalar_one()
    # 查找并删除指定的记录
    if del_obj:
        db.session.delete(del_obj)
        db.session.commit()
        return jsonify({'message': 'Record of Player deleted successfully'}), 200
    else:
        return jsonify({'error': 'Record of Player not found'}), 404

@app.route('/Database_add',methods=['GET', 'POST'])
def add_data_from_csv():
    """Adds data to the database if it does not already exist."""
    dataframe = pd.read_csv("E:\Programming_Assignments\comp0034-cw1i-King-in-black\src\data\data.csv")
    dataframe.columns.values[0] = 'Data_ID'
    print("Start adding IMU data to the database")
    records = dataframe.to_dict(orient='records')
    # converts to the dictionary
    for datarow in records:
        data_row = Data(**datarow)  # 使用字典解包创建Trainer实例
        db.session.add(data_row)
    db.session.commit()
@app.route('/')



"""
@app.get('/Database_row')
@app.get('/Database_row')
@app.post('/Database_add')
@app.post("/Datarow_add")
@app.delete("/Datarow_get")
@app.delete("/Datarow_delete")
@app.delete("/Dataset_delete")
"""
# Run the app
if __name__ == '__main__':
    app.run(debug=True)