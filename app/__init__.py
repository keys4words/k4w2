from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "danger"


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.views import basic_routes
        app.register_blueprint(basic_routes)
        from app.admin.views import admin_routes
        app.register_blueprint(admin_routes)
        # db.create_all()
        return app