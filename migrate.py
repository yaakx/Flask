# -*- coding: utf-8 -*-

"""Migrations using alembic"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db

def my_migration():
    app = create_app()
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()

if __name__ == '__main__':
    my_migration()
