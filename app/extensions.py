##

## SQL Alchemy
from flask_sqlalchemy import Model, SQLAlchemy
class ORMModel(Model):
    def update(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

db = SQLAlchemy(model_class=ORMModel)


from flask_migrate import Migrate
migrate = Migrate()

## Restful API
from .helpers import AppApi
import types
api = AppApi(prefix='/api')


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper


api.route = types.MethodType(api_route, api)

## API Spec Docs
from flask_apispec import FlaskApiSpec
docs = FlaskApiSpec()


## Marshmallow
from flask_marshmallow import Marshmallow
ma = Marshmallow()

# JWT
from flask_jwt import JWT
jwt = JWT()

from flask_login import LoginManager
login_manager = LoginManager()
