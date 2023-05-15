# -*- coding: utf-8 -*-
# @Time: 2023/5/15 17:22
# @Author: lijunhui
# @File: __init__.py.py
"""
__init__.py.py
"""
from flask import Blueprint

simple_blue_print = Blueprint('simple_blue_print', __name__)

from blueprint_test import views
