# 基于登录创建token进行身份验证
# 实现多个装饰器的合并，减少每个view代码同时添加jwt和route的重复代码

from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

from functools import wraps

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

jwt = JWTManager(app)


@app.route('/')
def index():
    return 'hello flask app'


@app.route('/login', methods=['POST'])
def login():
    """
    Returns a JWT token.
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "app Bad username or password"}), 401

    access_token = create_access_token(identity=username)



def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def composed_route_and_jwt_required(rule: str, **options):
    def dec_jwt(optional: bool = False,
                fresh: bool = False,
                refresh: bool = False,
                locations=None,
                verify_type: bool = True,):
        def decorator(f):
            jwt_dec = jwt_required(
                optional=optional, fresh=fresh, refresh=refresh, locations=locations, verify_type=verify_type)
            route_dec = app.route(rule, **options)
            return composed(route_dec, jwt_dec)(f)

        return decorator
    return dec_jwt


def jwt_and_route(rule: str, **options):
    def dec_jwt(optional: bool = False,
                fresh: bool = False,
                refresh: bool = False,
                locations=None,
                verify_type: bool = True,):
        def decorator(f):
            jwt_dec = jwt_required()
            route_dec = app.route(rule, **options)

            @wraps(f)
            @route_dec
            @jwt_dec
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return decorator
    return dec_jwt


def simple_route_and_jwt_required(rule: str, **options):
    jwt_option = options.pop("jwt_options", {})

    def decorator(fn):
        @wraps(fn)
        @app.route(rule, **options)
        @jwt_required(**jwt_option)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper

    return decorator


@simple_route_and_jwt_required("/protected", methods=["GET"], jwt_options={"optional": True})
def protected():
    """
    Returns a protected response.
    """
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200


if __name__ == '__main__':
    app.run(debug=True)
# test
# $ curl -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}' http://localhost:5000/login
# {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2....
# $ curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:5000/protected
