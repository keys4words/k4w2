from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from app import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        user = User.query.filter_by(username=request.form['login']).first()
        
        if not user:
            flash('There is NO user with this login!')
            return render_template('login.html')
        
        flash('You are successfully logged in!')
        login_user(user, remember=True)

        if 'next' in session:
            next = session['next']
        if is_safe_url(next) and next is not None:
            return redirect(next)
    return render_template('login.html')
    
    # session['next'] = request.args.get('next')
    # return render_template('login.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/projects/<int:id>')
@login_required
def project(id):
    return str(id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('There is NO user with this username!')
    return redirect(url_for('main.index'))


@app.route('/admin')
@login_required
def admin_page():
    if current_user.role == 'admin':
        flash('Welcome, admin')
        return render_template('main/admin_page.html')
    flash('You need to have Admin priveledges!')
    return redirect(url_for('login'))