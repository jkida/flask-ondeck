import datetime


# database connection data
DB_CONNECTION = {
    'SQLALCHEMY_DATABASE_URI': 'postgresql://ondeck:dev@localhost/ondeckmgr',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # "MONGODB_DB": "development",
    # "MONGODB_USERNAME": "",
    # "MONGODB_PASSWORD": "",
    # "MONGODB_HOST": "localhost",
    # "MONGODB_PORT": 27017
}

# flask vars
FLASK_VARS = {
    'DEBUG': True,
    'SECRET_KEY': 'aReallySecretKey',
}

# flask-jwt vars
FLASK_JWT_VARS = {
    'JWT_AUTH_URL_RULE': '/api/auth',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}

# flask-apispec
FLASK_API_SPEC = {
    'APISPEC_TITLE': 'OnDeck Manager API',
    'APISPEC_VERSION': 'v1',
    'APISPEC_SWAGGER_UI_URL': '/swagger/',
    'APISPEC_SWAGGER_URL': '/swagger-json/'
}

# another third party libs...
PASSLIB = {
    'HASH_ALGORITHM': 'SHA512',
    'HASH_SALT': 'HiMyNameIsGoku',
}
