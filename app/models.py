from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Unicode(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User {self.login}>"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
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
