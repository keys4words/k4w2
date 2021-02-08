from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextField, SubmitField

class AddProjectForm(FlaskForm):
    pr_img = StringField('Path to img')
    name = StringField('Project name')
    short_desc = StringField('Project short description')
    stack = StringField('Stack')
    long_desc = TextField('Project full description')
    live_anchor = StringField('Live web-site anchor')
    github_anchor = StringField('Github anchor')
    submit = SubmitField("Add Project")
