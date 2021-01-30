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
    pr_img = db.Column(db.String(255))
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    short_desc = db.Column(db.String(255), nullable=False, server_default=u'')
    long_desc = db.Column(db.Text, nullable=False, server_default=u'')
    live_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)
    github_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)

    def __init__(self, name, pr_img, short_desc, long_desc, live_anchor, github_anchor):
        self.name = name
        if pr_img:
            self.pr_img = pr_img
        else:
            self.pr_img = 'https://source.unsplash.com/random/301x200'
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.live_anchor = live_anchor
        self.github_anchor = github_anchor

    def __repr__(self):
        return f'<Project {self.name}>'


def seed_db(db):
    db.create_all()
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

    pr1 = Project('FAQ App', None, 'Simple flask web-app with authorization - for answer-question logic. Postgress + pure flask without any extensions. 3 level of users: admin, experts and users.',
     '''Simple flask web-app with authorization - for answer-question logic. Postgress + pure flask without any extensions. 3 level of users: admin, experts and users.

    Users are able ask questions to definite experts after registration. There 3 users with names: user, user2, user3 and the same passwords = ‘test’.

    Experts are able answer appropriate questions after approving their expert status by admin.
    There are 2 experts with names: expert, expert2 and same passwords = ‘test’.

    Admin see all users and may approve expert status for definite expert.
    ''', 'https://nameless-woodland-28899.herokuapp.com/', 'https://github.com/keys4words/faq.git')

    pr2 = Project('Real estate App', None, 'Django ecomm web-service for real estate','lorem ipsum','', '')
    pr3 = Project('Flask Landing', None, 'Flask landing page with signup form',
     '''Landing page with signup form - to get subscribers.
        Stack - flask + sqlite3 + email-extension.
     ''', 'https://my-looplab.herokuapp.com/', 'https://github.com/keys4words/looplab.git')
    pr4 = Project('Flask API', None, 'Flask API with auth - GET/POST/PUT/PATCH/DELETE support',
     '''Create app on base sqlite db with base authorization (username=’admin’, password=’admin’). 
        See all users = GET http://keys4.pythonanywhere.com/member
        Add new user = POST http://keys4.pythonanywhere.com/member need json object kinda
        {
            "name": "john dow",
            "email": "j.dow@mail.com",
            "level": "Bronze"
        }
        See user  = GET http://keys4.pythonanywhere.com/member/<id>
        Return json kinda
        {
            "member": {
                "email": "s.connor@mail.com",
                "id": 2,
                "level": "Silver",
                "name": "Sara Connor"
            }
        }
        Update user = PUT, PATCH http://keys4.pythonanywhere.com/member/<id>
        Return refreshed json kinda
        {
            "member": {
                "email": "s.connor@mail.com",
                "id": 2,
                "level": "Silver",
                "name": "Sara Connor"
            }
        }
        Delete user = DELETE http://keys4.pythonanywhere.com/member/<id>
        Return json kinda
        {
            "message": “The member has been deleted!”
        }
    ''', 'http://keys4.pythonanywhere.com/', 'https://github.com/keys4words/flaskApi.git')

    db.session.add_all([pr1, pr2, pr3, pr4])
    db.session.commit()

