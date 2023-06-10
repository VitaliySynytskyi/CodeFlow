# app.py
import logging
from datetime import datetime, timedelta
import os
import emoji
from flask import Flask, render_template, redirect, flash, send_from_directory, url_for, session, request, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from authlib.integrations.flask_client import OAuth
from applicationinsights.flask.ext import AppInsights

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = os.urandom(12)

logging.basicConfig(filename='app.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)

oauth = OAuth(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
swagger = Swagger(app)
appinsights = AppInsights(app)
app.jinja_env.filters['emojize'] = emoji.emojize
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Move your route handlers to the bottom of the file

# Import your route handlers from separate files
from home import *
from cats import *
from authentication import *
from blog import *
from profile_1 import *


if __name__ == "__main__":
    app.run(host='0.0.0.0')
