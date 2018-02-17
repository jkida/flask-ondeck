import datetime
from functools import wraps

from flask import current_app
from app import helpers, models

from flask_jwt import verify_jwt
from flask_apispec import MethodResource



def jwt_required(realm=None):
    """View decorator that requires a valid JWT token to be present in the request

    :param realm: an optional realm
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt(realm)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def jwt_require_all(cls):
    for meth in ('get', 'post', 'put', 'patch', 'delete'):
        if hasattr(cls, meth):
            setattr(cls, meth, jwt_required()(getattr(cls, meth)))
    return cls


def set_jwt_handlers(jwt):
    """Define handlers to jwt.

    :jwt: flask_jwt.JWT object
    :returns: None

    """

    @jwt.authentication_handler
    def authenticate(username, password):
        user = models.User.query.filter(models.User.username == username).first()
        if user and helpers.verify_password(password, user.password):
            return user
        return None

    @jwt.error_handler
    def error_handler(error):
        return 'Auth Failed: {}'.format(error.description), 400

    @jwt.payload_handler
    def make_payload(user):
        return {
            'user_id': str(user.id),
            'exp': (datetime.datetime.utcnow() +
                    current_app.config['JWT_EXPIRATION_DELTA']).isoformat()
        }

    @jwt.user_handler
    def load_user(payload):
        return models.User.query.filter_by(id=payload['user_id']).first()

