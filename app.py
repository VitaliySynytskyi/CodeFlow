import logging
from applicationinsights.flask.ext import AppInsights
from flasgger import Swagger
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
swagger = Swagger()
appinsights = AppInsights()
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = Config.APPINSIGHTS_INSTRUMENTATIONKEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    appinsights.init_app(app)
    swagger.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    
    return app

