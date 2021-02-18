from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, SelectMultipleField
from app.models import default_tags

class AddProjectForm(FlaskForm):
    pr_img = StringField('Path to img')
    name = StringField('Project name')
    short_desc = TextAreaField('Project short description')
    tags = SelectMultipleField('Available tags', choices=default_tags())
    long_desc = TextAreaField('Project full description')
    live_anchor = StringField('Live web-site anchor')
    github_anchor = StringField('Github anchor')
    submit = SubmitField("Add Project")
