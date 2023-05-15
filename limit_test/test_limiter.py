# -*- coding: utf-8 -*-
# @Time: 2023/5/15 17:46
# @Author: lijunhui
# @File: test_limiter.py
"""
test_limiter.py
"""

# 测试limiter的效果
from flask import Flask, Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# 载入蓝图
from blueprint_test import simple_blue_print

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

limiter.limit("1 per minute")(simple_blue_print)
app.register_blueprint(simple_blue_print, url_prefix="/")

# 获取所有已经注册的 URL 规则和对应的视图函数
for rule in app.url_map.iter_rules():
    view_func = app.view_functions.get(rule.endpoint)
    print(rule, view_func)

# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
