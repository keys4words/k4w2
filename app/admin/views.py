import random
from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from app.models import db, User, Project, Tag

from app.forms import AddProjectForm


admin_routes = Blueprint('admin_routes', __name__, url_prefix='/admin', template_folder='templates')



def find_tag_by_name(lst, search_name):
        for el in lst:
            if el.name == search_name:
                return el
        return False


def superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.is_admin:
                flash('You need to have Admin priveledges!', category='danger')
                return redirect(url_for('basic_routes.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_routes.route('/', methods=['GET', 'POST'])
@superuser
def cms():
    if request.method == 'POST':
        id = request.form.get('project_to_del')
        if id:
            project_to_del = Project.query.get(int(id))
            db.session.delete(project_to_del)
            db.session.commit()
            flash(f'Project was successfully deleted!', category='info')

    projects = Project.query.all()
    return render_template('cms.html', projects=projects)


@admin_routes.route('/addproject', methods=['GET', 'POST'])
@superuser
def add_project():
    form = AddProjectForm()
    if request.method == 'POST':
        print('in add_project POST method')
        pr_img = request.form.get('pr_img')
        name = request.form.get('name')
        short_desc = request.form.get('short_desc')
        tags_from_form = request.form.get('tags')
        all_tags = Tag.query.all()
        tags_name_list = [tag.name for tag in all_tags]
        
        if tags_from_form is None:
            tags_from_form = tags_name_list

        real_tags = [find_tag_by_name(all_tags, el) for el in tags_from_form if el in tags_name_list]

        long_desc = request.form.get('long_desc')
        live_anchor = request.form.get('live_anchor')
        github_anchor = request.form.get('github_anchor')

        new_project = Project(name, pr_img, short_desc, long_desc, live_anchor, github_anchor)
        new_project.tags.extend(real_tags)
        db.session.add(new_project)
        db.session.commit()
        flash(f'Project {name} was successfully added!', category='info')
        return redirect(url_for('admin_routes.cms'))
        
    return render_template('add_project.html', form=form, h4='Add new project', action="Add project")


@admin_routes.route('/<int:project_id>', methods=['GET', 'POST'])
@superuser
def edit_project(project_id):
    project_to_update = Project.query.get(project_id)
    form = AddProjectForm(obj=project_to_update)
    tags = Tag.query.all()
    tags_name_list = [tag.name for tag in tags]
    
    if form.validate_on_submit():
        project_to_update.pr_img = form.pr_img.data
        project_to_update.name = form.name.data
        project_to_update.short_desc = form.short_desc.data
        project_to_update.tags = [find_tag_by_name(tags, el) for el in form.tags.data if el in tags_name_list]
        project_to_update.long_desc = form.long_desc.data
        project_to_update.live_anchor = form.live_anchor.data
        project_to_update.github_anchor = form.github_anchor.data

        db.session.commit()
        flash(f'Project {project_to_update.name} was successfully updated!', category='info')
        return redirect(url_for('admin_routes.cms'))
        
    return render_template('add_project.html', form=form, h4='Edit project', action="Save changes")


@admin_routes.route('/addtag/<tag_name>')
@superuser
def add_tag(tag_name):
    bg_list = ['primary', 'secondary', 'warning', 'danger', 'success', 'info', 'light', 'dark']
    new_tag = Tag(name=tag_name, bg=random.choice(bg_list))
    db.session.add(new_tag)
    db.session.commit()
    flash(f'Tag {tag_name} was successfully added!', category='info')
    return redirect(url_for('admin_routes.cms'))