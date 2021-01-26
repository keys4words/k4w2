from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
login_manager = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404


from .views import register_blueprints
register_blueprints(app)

from .models.user_models import User
from .models.project_models import Project