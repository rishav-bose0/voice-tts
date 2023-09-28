import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import app_config
from common.model import db
from web.base import create_app


config_dict = app_config
app = create_app(config_dict)

MIGRATION_DIR = os.path.join('migrations')

migrate = Migrate(app, db, MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
