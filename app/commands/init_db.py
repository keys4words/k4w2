# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin')

    # Add users
    user = find_or_create_user(u'admin', 'secret', admin_role)
    user = find_or_create_user(u'guest', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
    return role


def find_or_create_user(login, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.login == login).first()
    if not user:
        user = User(login=login,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True)
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user



