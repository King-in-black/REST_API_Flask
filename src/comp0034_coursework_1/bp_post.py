@app.route('/player_add',methods=['GET', 'POST'])
def create_player():
    try:

        player_json = request.get_json()
        player = Player_Schema.load(player_json)
        db.session.add(player)
        db.session.commit()
        return jsonify({"message": f"Player added with the player_ID={player.Player_ID}"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.post('/trainer_add')
def create_trainer():
    '''

        The database will be requested to add the information of the trainer(ID and password)
         with the json file
        :return: the message of the trainer with certain trainer_ID is added successfully.

    '''
    trainer_json=request.get_json()
    print(trainer_json)
    trainer= Trainer_Schema.load(trainer_json)
    print(trainer)
    db.session.add(trainer)
    db.session.commit()
    return {"message":f"Trainer added with the trainer_ID={trainer.Trainer_ID}"}

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
