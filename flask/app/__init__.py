from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import db, User, seed_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')

    login_manager = LoginManager()
    login_manager.login_view = "basic_routes.login"
    login_manager.login_message_category = "danger"

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    def is_safe_url(target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template('404.html'), 404


    with app.app_context():
        # db.create_all()
        # seed_db(db)

        from app.views import basic_routes
        app.register_blueprint(basic_routes)
        from app.admin.views import admin_routes
        app.register_blueprint(admin_routes)
        return app
