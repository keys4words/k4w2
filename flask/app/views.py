from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from app.models import User, Project, Tag
from app.forms import SimpleForm


basic_routes = Blueprint('basic_routes', __name__)


def check_tags(filter, project):
    tags = [str(tag) for tag in project.tags]
    return (filter in tags)


@basic_routes.route('/')
def home():
    return render_template('home.html')

@basic_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=request.form['login']).first()
            if user:
                if check_password_hash(user.password, password):
                    if user.is_admin:
                        login_user(user, remember=True)
                        flash('Hey, Admin!', category='info')
                        return redirect(url_for('admin_routes.cms'))
                        
                    else:
                        flash('You are successfully log in!', category='info')
                        login_user(user, remember=True)
                   
                        next_page = request.args.get('next')
                        if next_page:
                            return redirect(next_page)
                        return redirect(url_for('basic_routes.projects', filter='All'))
                else:
                    flash('Wrong password!', category='danger')
            else:
                flash('There is NO user with this login!', category='danger')
                return render_template('login.html')
        else:
            flash('Please fill in login and password', category='danger')
    return render_template('login.html')
    

@basic_routes.route('/projects/<filter>')
def projects(filter):
    projects = Project.query.all()
    if filter != 'All':
        projects = [project for project in projects if check_tags(filter, project)]
    tags = Tag.query.all()
    return render_template('projects.html', projects=projects, tags=tags)


@basic_routes.route('/project/<int:id>')
@login_required
def project(id):
    project = Project.query.filter_by(id=id).first()
    return render_template('project.html', project=project)


@basic_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!', category='info')
    return redirect(url_for('basic_routes.home'))


@basic_routes.route('/form',methods=['post','get'])
def hello_world():
    form = SimpleForm()
    if form.validate_on_submit():
        print(form.example.data)
        return render_template("success.html", data=form.example.data)
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('example.html',form=form)