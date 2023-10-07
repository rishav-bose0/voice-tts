from flask import Blueprint, Flask
from flask_restx import Api
from web.routing import routes
from common.model import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1.0', title='TTS Api', description='TTS Web Api')


def set_db_config(config):
    config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": config["POOL_PRE_PING"],
                                           "pool_timeout": config["POOL_TIMEOUT"],
                                           "max_overflow": config["MAX_OVERFLOW"],
                                           "pool_size": config["POOL_SIZE"]}
    config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{config["DB_USERNAME"]}:' \
                                        f'{config["DB_PASSWORD"]}@{config["DB_HOST"]}:' \
                                        f'{config["DB_PORT"]}/{config["DB_DATABASE"]}'


def create_app(config=None):
    app = Flask(__name__)
    set_db_config(config)
    app.config.update(config or {})
    db.init_app(app)
    routes.add_default_routes(api)
    routes.add_tts_api_routes(api)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app

