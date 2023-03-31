from datetime import datetime
import os
from flasgger import Swagger
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY') or 'a4f728a4c7cb3be47a9e8326d23f6edf'
swagger = Swagger(app)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # тут буде логіка для перевірки даних з форми
        # та входу користувача на сайт ок зроз?
        flash('You have been logged in!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/hello')
def hello():
    """
    A sample endpoint that returns a greeting.
    ---
    responses:
      200:
        description: A string indicating a greeting.
    """
    return 'Hello, world!'


@app.route('/')
def home():
    print('Request for index page received')
    return render_template('home.html')


@app.route('/about')
def about():
    print('Request for about page received')
    return render_template('about.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route('/hello', methods=['POST'])
# def hello():
#     name = request.form.get('name')

#     if name:
#         print('Request for hello page received with name=%s' % name)
#         return render_template('hello.html', name=name)
#     else:
#         print('Request for hello page received with no name or blank name -- redirecting')
#         return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
