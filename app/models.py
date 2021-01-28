from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Unicode(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, login, password, active):
        self.login = login
        self.password = generate_password_hash(password)
        self.active = active

    def __repr__(self):
        return f"<User {self.login}>"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'


class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id



class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    short_desc = db.Column(db.String(255), nullable=False, server_default=u'')
    long_desc = db.Column(db.Text, nullable=False, server_default=u'')
    live_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)
    github_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)

    def __init__(self, name, short_desc, long_desc, live_anchor, github_anchor):
        self.name = name
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.live_anchor = live_anchor
        self.github_anchor = github_anchor

    def __repr__(self):
        return f'<Project {self.name}>'


def seed_db(db):
    admin_role = Role('admin')
    guest_role = Role('guest')
    db.session.add_all([admin_role, guest_role])
    db.session.commit()

    pass_4_admin = input('Input pass for Admin: ')
    pass_4_guest = input('Input pass for guest: ')
    admin = User('superAdmin', pass_4_admin, True)
    guest = User('guest', pass_4_guest, True)
    db.session.add_all([admin, guest])
    db.session.commit()

    admin_role_assign = UsersRoles(admin.id, admin_role.id)
    guest_role_assign = UsersRoles(guest.id, guest_role.id)
    db.session.add_all([admin_role_assign, guest_role_assign])
    db.session.commit()



