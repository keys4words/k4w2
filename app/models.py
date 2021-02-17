from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Unicode(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, login, password):
        self.login = login
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.login}>"
    
    def make_inactive(self):
        self.active = False


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer(), primary_key=True)
    pr_img = db.Column(db.String(255))
    name = db.Column(db.String(50))
    short_desc = db.Column(db.String(255))
    long_desc = db.Column(db.Text)
    live_anchor = db.Column(db.String(150))
    github_anchor = db.Column(db.String(150))

    tags = db.relationship('Tag', backref='list', lazy='dynamic')

    def __init__(self, name, pr_img, short_desc, long_desc, live_anchor, github_anchor):
        self.name = name
        self.pr_img = pr_img
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.live_anchor = live_anchor
        self.github_anchor = github_anchor

    def __repr__(self):
        return f'<Project {self.name}>'


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    bg = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, name, bg):
        self.name = name
        self.bg = bg

    def __repr__(self):
        return f'{self.name}'



def seed_db(db):
    db.create_all()

    pass_4_admin = input('Input pass for Admin: ')
    pass_4_guest = input('Input pass for guest: ')
    admin = User('superAdmin', pass_4_admin)
    admin.is_admin = True
    guest = User('guest', pass_4_guest)
    db.session.add_all([admin, guest])
    db.session.commit()

    flask = Tag('Flask', bg='primary')
    dbs = Tag('Postgress', bg='secondary')
    html = Tag('HTML/CSS', bg='warning')
    django = Tag('Django', bg='danger')
    api = Tag('API', bg='success')
    php = Tag('PHP', bg='info')
    js_stack = Tag('JS', bg='light')
    scraping = Tag('Web-scraping', bg='dark')

    db.session.add_all([flask, dbs, html, django, api, php, js_stack])
    db.session.commit()

    pr1 = Project('FAQ App', 'pr1.jpg', 'Simple flask web-app with authorization - for answer-question logic.\nPostgress + pure flask without any extensions.\n 3 level of users: admin, experts and users.',
     '''Simple flask web-app with authorization - for answer-question logic. Postgress + pure flask without any extensions. 3 level of users: admin, experts and users.

    Users are able ask questions to definite experts after registration. There 3 users with names: user, user2, user3 and the same passwords = ‘test’.

    Experts are able answer appropriate questions after approving their expert status by admin.
    There are 2 experts with names: expert, expert2 and same passwords = ‘test’.

    Admin see all users and may approve expert status for definite expert.
    ''', 'https://nameless-woodland-28899.herokuapp.com/', 'https://github.com/keys4words/faq.git')

    pr1.tags.extend([flask, dbs])
    db.session.add(pr1)
    db.session.commit()
    
    pr2 = Project('Pulse', 'pr2.jpg', 'Ecom', '', '', 'https://github.com/keys4words/pulse')
    pr2.tags.extend([html, js_stack, php])
    db.session.add(pr2)
    db.session.commit()

    pr3 = Project('Real estate App', 'pr3.jpg', 'Django ecomm web-service for real estate','lorem ipsum','', '')
    pr3.tags.extend([django, dbs])
    db.session.add(pr3)
    db.session.commit()

    pr4 = Project('Flask Landing', 'pr4.jpg', 'Flask landing page with signup form', 
     '''Landing page with signup form - to get subscribers.
     ''', 'https://my-looplab.herokuapp.com/', 'https://github.com/keys4words/looplab.git')
    pr4.tags.extend([flask, dbs])
    db.session.add(pr4)
    db.session.commit()

    pr5 = Project('Flask API', 'pr5.jpg', 'Flask API with auth - GET/POST/PUT/PATCH/DELETE support',
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

    pr5.tags.extend([flask, dbs, api])
    db.session.add(pr5)
    db.session.commit()

    pr6 = Project('Tender scraping', 'pr6.jpg', 'Bunch of web-scrapers government tenders', '', '', 'https://github.com/keys4words/tenders')
    pr6.tags.extend([dbs, scraping])
    db.session.add(pr6)
    db.session.commit()

