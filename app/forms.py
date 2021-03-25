from flask_wtf import FlaskForm
from wtforms import widgets, StringField, IntegerField, SubmitField, TextAreaField, SelectMultipleField
from app.models import default_tags


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SimpleForm(FlaskForm):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    files = [('0', 'first element'), (2, 'two'), (3, 'three')]
    example = MultiCheckboxField('Label', choices=files)

class AddProjectForm(FlaskForm):
    pr_img = StringField('Path to img')
    name = StringField('Project name')
    short_desc = TextAreaField('Project short description')
    tags = SelectMultipleField('Available tags', choices=default_tags())
    long_desc = TextAreaField('Project full description')
    live_anchor = StringField('Live web-site anchor')
    github_anchor = StringField('Github anchor')
    submit = SubmitField("Add Project")

