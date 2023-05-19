# -*- coding: utf-8 -*-
# @Time: 2023/5/19 13:30
# @Author: lijunhui
# @File: db_connect.py
"""
db_connect.py
"""

from sqlalchemy import create_engine

test_conn = create_engine('sqlite:///instance/project.db')

# 监听engine
from sqlalchemy_test.watch_long_sql import monitor_engine

# monitor_engine(engine)