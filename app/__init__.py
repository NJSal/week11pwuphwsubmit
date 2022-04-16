"""A simple flask web app"""
#import flask_login
import os
#from logging.handlers import RotatingFileHandler

import flask_login
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

from app.auth import auth
#from app.auth import auth
#from app.cli import create_database, create_log_folder
from app.cli import create_database
from app.context_processors import utility_text_processors
from app.db import db
from app.db.models import User
#from app.error_handlers import error_handlers
from app.exceptions import http_exceptions

#from app.logging_config import log_con
from app.simple_pages import simple_pages

import logging

#from flask.logging import default_handler

login_manager = flask_login.LoginManager()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    logging.basicConfig(filename='logs/record.log', level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    app.config['WTF_CSRF_ENABLED'] = False

    bootstrap = Bootstrap5(app)
    app.register_blueprint(simple_pages)
    app.register_blueprint(auth)
    app.context_processor(utility_text_processors)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'Simplex'
    app.register_error_handler(404, page_not_found)
    # app.add_url_rule("/", endpoint="index")
    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # add command function to cli commands
    app.cli.add_command(create_database)

    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
