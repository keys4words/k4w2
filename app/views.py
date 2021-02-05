from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from app import app, db, login_manager
from app.models import User, Project


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.roles[0].name != 'admin':
                flash('You need to have Admin priveledges!', category='danger')
                redirect(url_for('login'))
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=request.form['login']).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('You are successfully log in!', category='info')
                    login_user(user, remember=True)
                   
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect(url_for('projects'))
                else:
                    flash('Wrong password!', category='danger')
            else:
                flash('There is NO user with this login!', category='danger')
                return render_template('login.html')
        else:
            flash('Please fill in login and password', category='danger')
    return render_template('login.html')
    

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)


@app.route('/projects/<int:id>')
@login_required
def project(id):
    project = Project.query.filter_by(id=id).first()
    return render_template('project.html', project=project)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!', category='info')
    return redirect(url_for('index'))


@app.route('/admin')
@superuser
def projects_list():
    projects = Project.query.all()
    return render_template('admin_page.html', projects=projects)


@app.route('/admin/add')
@superuser
def admin_add_project():
    return render_template('add_project.html')