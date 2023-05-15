# Description: 测试monkey_patch_jwt.py的效果

import monkey_patch_jwt
from flask_jwt_extended import jwt_required, verify_jwt_in_request, JWTManager
from flask import Flask
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
jwt = JWTManager(app)


def route(url, methods=None):
    """
    代替原本的route函数，添加了methods默认选项为['POST', 'GET'],而不是['GET']

    :param url:
    :param methods:
    :return:
    """
    method_list = methods if methods else ['POST', 'GET']
    return app.route(url, methods=method_list)


@app.before_request
def before_request():
    print("before_request")


@route("/")
def index():
    return 'index'


@route("/test-jwt")
@jwt_required()
def jwt_test():
    return 'jwt-test'


@route("/test-verify")
def test_verify():
    verify_jwt_in_request()
    return 'test-verify'


if __name__ == '__main__':
    app.run()
