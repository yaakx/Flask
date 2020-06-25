# -*- coding: utf-8 -*-

"""Create app program"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    """Create app for importing to the other programs"""

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gotuser:julenflask@localhost/got'
    db.init_app(app)
    return app
