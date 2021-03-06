import flask
from . import extensions, config, models
from .users import resources
from .queueboards import resources
from .auth import jwt
from app.auth.redis_session import RedisSessionInterface, set_session_handlers
from .helpers import TimeRange
from psycopg2.extras import register_range


def create_app(config_name='default'):
    """Flask app factory

    :config_name: a string object.
    :returns: flask.Flask object

    """

    app = flask.Flask(__name__)

    # set the config vars using the config name and current_app
    config.config[config_name](app)

    register_extensions(app)

    jwt.set_jwt_handlers(extensions.jwt)
    app.session_interface = RedisSessionInterface()
    set_session_handlers()

    @app.before_first_request
    def add_time_range_type():
        conn = extensions.db.engine.raw_connection()
        cur = conn.cursor()
        register_range('timerange', TimeRange, cur, globally=True)
        cur.close()
        conn.close()

    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None

    """

    extensions.db.init_app(app)
    extensions.jwt.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.api.init_app(app)
    extensions.docs.init_app(app)
    extensions.ma.init_app(app)


