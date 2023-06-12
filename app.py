# app.py
import argparse
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

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=31)

from home import *
from cats import *
from authentication import *
from blog import *
from profile_1 import *

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

from flask_migrate import Migrate, upgrade, init, stamp

def deploy():
    """Run deployment tasks."""
    with app.app_context():
        db.create_all()

        # migrate database to latest revision
        init(directory='migrations')
        stamp(directory='migrations')
        Migrate(directory='migrations')
        upgrade(directory='migrations')

def run_server():
    app.run(ssl_context="adhoc")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask server or perform deployment tasks.")
    parser.add_argument('command', choices=['run', 'deploy'], help="Either 'run' to start the server or 'deploy' to perform deployment tasks.")
    args = parser.parse_args()

    if args.command == 'run':
        run_server()
    elif args.command == 'deploy':
        deploy()