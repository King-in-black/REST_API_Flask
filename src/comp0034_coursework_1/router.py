# Import the Flask class from the Flask library
from flask import Flask ,request ,redirect , url_for, render_template
from .import create_app
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

@app.route('/register')
def register():
    # The function returns the message we want to display in the user’s browser. The default content type is HTML,
    # so HTML in the string will be rendered by the browser.
    return 'Hello World re!'

@app.route('/login')
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