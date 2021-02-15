from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from app import db, login_manager
from app.models import User, Project

from app.forms import AddProjectForm


admin_routes = Blueprint('admin_routes', __name__, url_prefix='/admin', template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.roles[0].name != 'admin':
                flash('You need to have Admin priveledges!', category='danger')
                return redirect(url_for('basic_routes.login'))
        return f(*args, **kwargs)
    return decorated_function


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


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


@admin_routes.route('/add', methods=['GET', 'POST'])
@superuser
def add_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        pr_img = form.pr_img.data
        name = form.name.data
        short_desc = form.short_desc.data
        stack = form.stack.data
        long_desc = form.long_desc.data
        live_anchor = form.live_anchor.data
        github_anchor = form.github_anchor.data

        new_project = Project(name, pr_img, short_desc, stack, long_desc, live_anchor, github_anchor)
        db.session.add(new_project)
        db.session.commit()
        flash(f'Project {name} was successfully added!', category='info')
        return redirect(url_for('admin_routes.cms'))
        
    return render_template('add_project.html', form=form, h4='Add new project', action="Add project")


@admin_routes.route('/<int:project_id>', methods=['GET', 'POST'])
@superuser
def edit_project(project_id):
    if request.method == 'GET':
        project_to_update = Project.query.get(project_id)
        form = AddProjectForm(obj=project_to_update)
    elif form.validate_on_submit():
        project_to_update.pr_img = form.pr_img.data
        project_to_update.name = form.name.data
        project_to_update.short_desc = form.short_desc.data
        project_to_update.stack = form.stack.data
        project_to_update.long_desc = form.long_desc.data
        project_to_update.live_anchor = form.live_anchor.data
        project_to_update.github_anchor = form.github_anchor.data

        db.session.commit()
        flash(f'Project {name} was successfully updated!', category='info')
        return redirect(url_for('admin_routes.cms'))
        
    return render_template('add_project.html', form=form, h4='Edit project', action="Save changes")
