from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from app import db, login_manager


main_blueprint = Blueprint('main', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            return 'There is NO user with this username!'
        login_user(user, remember=True)
        if 'next' in session:
            next = session['next']
            
            if is_safe_url(next) and next is not None:
                return redirect(next)

        return 'You are successfully logged in!'
    
    session['next'] = request.args.get('next')
    return render_template('login.html')


@main_blueprint.route('/projects')
def projects():
    return render_template('projects.html')


@main_blueprint.route('/projects/<int:id>')
@login_required
def project(id):
    return str(id)


@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main_blueprint.route('/admin')
def admin_page():
    return render_template('main/admin_page.html')