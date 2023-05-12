
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

oidc_auth = False


def optional_verify_jwt_in_request(fresh=False, refresh=False, locations=None):
    from flask_jwt_extended import verify_jwt_in_request as _verify_jwt_in_request
    return _verify_jwt_in_request(optional=True, fresh=fresh, refresh=refresh, locations=locations)


if not oidc_auth:
    logger.warning("unauth now")
    verify_jwt_in_request = optional_verify_jwt_in_request


def optional_jwt_required(fresh=False, refresh=False, locations=None):
    return flask_jwt_extended.jwt_required(optional=True, fresh=fresh, refresh=refresh, locations=locations)


if not oidc_auth:
    logger.warning("unauth now")
    jwt_required = optional_jwt_required

# jwt

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'hello flask app'


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return 'hello protected'


if __name__ == '__main__':
    app.run(debug=True)
