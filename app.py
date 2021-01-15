from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, fresh_login_required


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
login_manager = LoginManager(app)
db = SQLAlchemy(app)


###############################
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


class UsersRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))



class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    short_desc = db.Column(db.String(255), nullable=False, server_default=u'')
    long_desc = db.Column(db.Text, nullable=False, server_default=u'')
    live_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)
    github_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)

###############################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
    return render_template('login.html')


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
    return redirect(url_for('index'))


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()