from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "danger"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views