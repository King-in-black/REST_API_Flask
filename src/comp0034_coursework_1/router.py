# Import the Flask class from the Flask library
# python -m src.comp0034_coursework_1.router
from flask import Flask ,request ,redirect , url_for, render_template,flash
from .import create_app
from .import db
from .models import Trainer,Player,Data
# Create an instance of a Flask application
# The first argument is the name of the application’s module or package. __name__ is a convenient shortcut.
# This is needed so that Flask knows where to look for resources such as templates and static files.
# Add a route for the 'home' page
# use the route() decorator to tell Flask what URL should trigger our function.
app = create_app()
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
        Player_ID = request.form['Player_ID']
        Trainer_ID = request.form['Trainer_ID']
        password = request.form['password']
        role = request.form['role']

        # 以下是将数据写入数据库的伪代码
        if role == 'player':
            # 创建Player实例并写入数据库
            new_user = Player(Trainer_ID=Trainer_ID, Player_ID=Player_ID, password=password)
            db.session.add(new_user)
        elif role == 'train':
            # 创建Trainer实例并写入数据库
            new_user = Trainer(Trainer_ID=Trainer_ID, Player_ID=Player_ID, password=password)
            db.session.add(new_user)
        else:
            flash('Please select a valid role', 'error')
            return render_template('register.html')

        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))  # 或其他页面

    return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    # The function returns the message we want to display in the user’s browser. The default content type is HTML,
    # so HTML in the string will be rendered by the browser.
    return 'Hello World loh!'

@app.route('/predict')
def predict():
    # The function returns the message we want to display in the user’s browser. The default content type is HTML,
    # so HTML in the string will be rendered by the browser.
    return 'Hello World!'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)