from datetime import datetime
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect


csrf_protect = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db.init_app(app)
migrate.init_app(app, db)
csrf_protect.init_app(app)


# Register blueprints
from .views import register_blueprints
register_blueprints(app)

# Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
from wtforms.fields import HiddenField

def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)

app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404

from .models.user_models import User
from .models.project_models import Project
from .views.main_views import user_profile_page

user_manager = UserManager(app, db, User)
