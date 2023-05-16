# -*- coding: utf-8 -*-
# @Time: 2023/5/15 17:04
# @Author: lijunhui
# @File: batch_protection_switch.py
"""
batch_protection_switch.py
实现对urls批量开启或关闭jwt保护
"""
import importlib
import typing
from functools import wraps

from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, \
    get_jwt_identity, verify_jwt_in_request, get_jwt
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 测试的路由，基于蓝图统一管理

from blueprint_test import simple_blue_print

jwt = JWTManager(app)
# jwt 配置
app.config["JWT_SECRET_KEY"] = "MYSECRETKEY"


# 改写成Class的方式，内部维护豁免的URLs


class TokenLimiter():
    """
    # token limit类，用于对urls进行批量开启或关闭jwt保护.
    # 1.支持蓝图、
    # 2.支持自定义校验函数
    # 3.支持正则匹配
    # 4.支持对普通URL注册
    # 用法：
    # 1.初始化TokenLimiter类，传入app(和permit_urls)
    # 2.调用register_token_limiter方法，传入蓝图和校验函数
    # 3.调用set_permit_urls方法，传入permit_urls
    """

    def __init__(self, app: Flask = None, ):
        self.app = app
        self.permit_urls = []

    def init_app(self, app: Flask = None):
        self.app = app

    def add_permit_url(self, permit_url: str = None):
        self.permit_urls.append(permit_url)

    def rm_permit_url(self, permit_url: str = None):
        self.permit_urls.remove(permit_url)

    # token limit检验函数
    def __inject_request(self, verify_fun: typing.Callable):
        """vefify的装饰函数，首先判断是否在豁免的urls中，若在则不进行token的校验"""

        @wraps(verify_fun)
        def wrapper(*args, **kwargs):
            # 判断是否在豁免的urls中
            request_endpoint = request.url_rule.endpoint
            import re
            for url_pattern in self.permit_urls:
                if re.match(url_pattern, request_endpoint):
                    logging.debug("skip token verify because of permit_urls")
                    return
            else:
                # 进行token的校验
                verify_fun(*args, **kwargs)

        return wrapper

    # 默认的校验函数
    @staticmethod
    def __default_verify_token_func():
        logging.debug('default_verify_token_func')
        verify_jwt_in_request()

    # 注册要处理的url或蓝图，对其注册验证处理
    def register_token_limiter(self, blueprint: Blueprint, verify_func: typing.Callable = None):
        # 判断用户是否制定校验函数，若没指定则设置为默认的
        if verify_func is None:
            verify_func = self.__default_verify_token_func

        # 注入校验函数到蓝图中，对其进行校验，若已经注册过则跳过
        try:
            blueprint.before_request(self.__inject_request(verify_func))
        except AssertionError:
            logging.warning(f"blueprint{blueprint.name} add verify_func failed, you have registered this blueprint!")


# 测试

# 自定义一个鉴权函数
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required():
    logging.info("admin required")
    verify_jwt_in_request()
    try:
        role = get_jwt().get('role')
        if role != 'admin':
            return {'msg': 'You are not authorized to access this resource'}, 403
    except Exception:
        return {'msg': 'Invalid token'}, 401
    logging.info("admin login")


# URLs注册Router
from CoreUtils.Conf import UrlDefine, BluePrintDefine, Conf

BLUEPRINT_CONFIG = {
    "simple_blue_print": Conf(module_name="blueprint_test", blueprint_name="simple_blue_print", is_verify_token=True,
                              verify_func=admin_required, ),
}

urlpatterns = [
    # UrlDefine(prefix="/", module_name="blueprint_test", blueprint_name="simple_blue_print", is_verify_token=True),
    # 　测试一个自定义的验证函数
    UrlDefine(prefix="/", config=BLUEPRINT_CONFIG.get("simple_blue_print")),
    UrlDefine(prefix="/simple", config=BLUEPRINT_CONFIG.get("simple_blue_print")),
]

blueprint_patterns = [BluePrintDefine(config=config) for _, config in BLUEPRINT_CONFIG.items()]

for blueprint in blueprint_patterns:
    # 获取蓝图对象
    bp = blueprint.get_blueprint()
    # TokenLimter
    limiter = TokenLimiter(app)
    limiter.add_permit_url(r"^.*test1")  # 豁免

    # 添加蓝图的鉴权处理
    if blueprint.get_is_verify_token():
        limiter.register_token_limiter(bp, blueprint.get_verify_func())

for url in urlpatterns:
    # 获取蓝图对象
    bp = url.get_blueprint()
    # 注册蓝图
    app.register_blueprint(bp, url_prefix=url.get_prefix(), name=url.get_prefix())


# 注册一个登陆的路由做测试
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # 创建token
    access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
    return jsonify(access_token=access_token)


# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)

# 废弃的思路：
# 1. 通过装饰器的方式，为每个视图函数添加装饰器。反过来也可以从里面拆掉装饰器
# def permit_url_from_token_request(url, app: Flask = None):
#     map = app.url_map
#     urls = [rule for rule in app.url_map.iter_rules()]
#     permit_urls = [rule for rule in app.url_map.iter_rules() if rule.endpoint == url]
#     # 获取所有已经注册的 URL 规则和对应的视图函数
#     for rule in permit_urls:
#         view_func = app.view_functions.get(rule.endpoint)
#         # print(rule, view_func)
#         # 为每个视图函数添加装饰器
#         # orginal_func = view_func.__wrapped__
#         # orginal_func()
#
#         # app.add_url_rule(rule.rule, endpoint=rule.endpoint, view_func=view_func, defaults=rule.defaults,
#         #                  subdomain=rule.subdomain, methods=rule.methods, redirect_to=rule.redirect_to,
#         #                  alias=rule.alias, host=rule.host,
#         #                  provide_automatic_options=rule.provide_automatic_options,
#         #                  strict_slashes=rule.strict_slashes, endpoint_arguments=rule.arguments,
#         #                  provide_automatic_options_for_non_get=rule.provide_automatic_options_for_non_get)
#
#     if url in permit_urls:
#
#         return True
#     else:
#         return False
