# -*- coding: utf-8 -*-
# @Time: 2023/5/15 17:04
# @Author: lijunhui
# @File: batch_protection_switch.py
"""
batch_protection_switch.py
实现对urls批量开启或关闭jwt保护
"""
import typing

from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, \
    get_jwt_identity, verify_jwt_in_request
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 测试的路由，基于蓝图统一管理

from blueprint_test import simple_blue_print

jwt = JWTManager(app)


def default_verify_token_func():
    verify_jwt_in_request()
    logging.debug('default_verify_token_func')


# 注册要处理的url或蓝图，对其注册验证处理
def register_token_limiter(blueprint, verify_func: typing.Callable = None):
    # 判断用户是否制定校验函数，若没指定则设置为默认的
    if verify_func is None:
        verify_func = default_verify_token_func
    # 判断用户输入的是蓝图还是url
    if True:
        blueprint.before_request(verify_func)

    if False:
        # 获取所有已经注册的 URL 规则和对应的视图函数
        for rule in blueprint.url_map.iter_rules():
            view_func = blueprint.view_functions.get(rule.endpoint)
            # print(rule, view_func)
            # 为每个视图函数添加装饰器
            view_func = jwt_required(view_func)
            blueprint.add_url_rule(rule.rule, endpoint=rule.endpoint, view_func=view_func, defaults=rule.defaults,
                                   subdomain=rule.subdomain, methods=rule.methods, redirect_to=rule.redirect_to,
                                   alias=rule.alias, host=rule.host,
                                   provide_automatic_options=rule.provide_automatic_options,
                                   strict_slashes=rule.strict_slashes, endpoint_arguments=rule.arguments,
                                   provide_automatic_options_for_non_get=rule.provide_automatic_options_for_non_get)


# @simple_blue_print.before_request
# def before_handle_request():
#     logging.info('before_request')
#     verify_jwt_in_request()


register_token_limiter(simple_blue_print, verify_func=lambda: logging.info('permit'))
app.register_blueprint(simple_blue_print, url_prefix='/')

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
