# -*- coding: utf-8 -*-
# @Time: 2023/5/16 16:22
# @Author: lijunhui
# @File: app_test1.py
"""
app_test1.py
"""
import random

from flask import Flask, jsonify, request
from flask_prometheus_metrics import register_metrics
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

users = ['Alice', 'Bob', 'Charlie']

# define custom metrics
metrics = {}

metrics['users'] = Counter(
    'users_total', 'Number of users')

metrics['add_user_requests'] = Counter(
    'add_user_requests_total', 'Number of add user requests.')

metrics['add_user_processing_time'] = Histogram(
    'add_user_processing_seconds', 'Add user request processing time', ['status'])


@app.route('/users', methods=['GET', 'POST'])
def add_user():
    users.append("username")

    # increment the custom metrics
    metrics['users'].inc()
    metrics['add_user_requests'].inc()
    # 随机生成一个0-10的数，作为延迟时间
    processing_time = random.random() / 10
    metrics['add_user_processing_time'].labels('success').observe(processing_time)
    return jsonify(success=True)


# register the custom metrics
# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="v0.1.2", app_config="staging")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

run_simple(hostname="localhost", port=5000, application=dispatcher)
