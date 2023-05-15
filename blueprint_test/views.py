# -*- coding: utf-8 -*-
# @Time: 2023/5/15 17:27
# @Author: lijunhui
# @File: views.py
"""
views.py
"""
from flask import jsonify

from blueprint_test import simple_blue_print


@simple_blue_print.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'msg': 'index'})


@simple_blue_print.route('/test1', methods=['GET', 'POST'])
def test1():
    return jsonify({'msg': 'test1'})


@simple_blue_print.route('/test2', methods=['GET', 'POST'])
def test2():
    return jsonify({'msg': 'test2'})


@simple_blue_print.route('/test3', methods=['GET', 'POST'])
def test3():
    return jsonify({'msg': 'test3'})
