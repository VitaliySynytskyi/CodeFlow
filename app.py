import os
import logging
from applicationinsights.flask.ext import AppInsights
from flasgger import Swagger
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from forms import LoginForm, RegistrationForm
from models import User
from config import Config


app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = Config.APPINSIGHTS_INSTRUMENTATIONKEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
swagger = Swagger(app)
appinsights = AppInsights(app)
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    logger.debug('Request for login page received')
    form = LoginForm()
    if form.validate_on_submit():
        # тут буде логіка для перевірки даних з форми
        # та входу користувача на сайт
        flash('You have been logged in!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug('Request for register page received')
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
    app.logger.info('Hello, World!')
    logger.debug('Entering hello string')
    return 'Hello, world!'


@app.route('/')
@app.route("/home")
def home():
    logger.debug('Request for index page received')
    return render_template('home.html')


@app.route('/about')
def about():
    logger.debug('Request for about page received')
    return render_template('about.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(port=8000)
