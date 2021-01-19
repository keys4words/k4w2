from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db


main_blueprint = Blueprint('main', __name__, template_folder='templates')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/login')
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
    return render_template('login.html')


@main_blueprint.route('/projects')
def projects():
    return render_template('projects.html')


@main_blueprint.route('/projects/<int:id>')
@login_required
def project(id):
    return str(id)



@main_blueprint.route('/logout')
def logout():
    return redirect(url_for('main.index'))

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile')
@login_required
def user_profile_page():

    # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)

    #     # Save user_profile
    #     db.session.commit()

    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)


