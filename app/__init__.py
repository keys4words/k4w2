from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
login_manager = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views, forms