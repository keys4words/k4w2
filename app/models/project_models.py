from app import db


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    short_desc = db.Column(db.String(255), nullable=False, server_default=u'')
    long_desc = db.Column(db.Text, nullable=False, server_default=u'')
    live_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)
    github_anchor = db.Column(db.String(150), nullable=False, server_default=u'', unique=True)