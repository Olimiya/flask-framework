import monkey_patch_jwt
from flask_jwt_extended import jwt_required, verify_jwt_in_request, JWTManager
from flask import Flask

test_flask_bp = Flask(__name__)
jwt = JWTManager(test_flask_bp)


def route(url, methods=None):
    """
    代替原本的route函数，添加了methods默认选项为['POST', 'GET'],而不是['GET']

    :param url:
    :param methods:
    :return:
    """
    method_list = methods if methods else ['POST', 'GET']
    return test_flask_bp.route(url, methods=method_list)


@route("/test-jwt")
@jwt_required()
def jwt_test():
    return 'jwt-test'


@route("/test-verify")
def test_verify():
    verify_jwt_in_request()
    return 'test-verify'


if __name__ == '__main__':
    test_flask_bp.run()
