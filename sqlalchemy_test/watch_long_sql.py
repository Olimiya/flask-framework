# -*- coding: utf-8 -*-
# @Time: 2023/5/17 13:56
# @Author: lijunhui
# @File: watch_long_sql.py
"""
watch_long_sql.py
实现对长SQL的监控
基于flask sqlachemy中的record_queries
另外实现：
1 添加读取配置进行控制的相关设置。
2 输出到日志，
3 添加阈值控制，进行报警
"""

import logging

# 设置
debug = True  # 是否开启debug模式
long_sql_threshold = 0.0001  # 长SQL阈值，单位秒


# region 监控实现，基于flask_sqlalchemy的record_queries

# 捕获SQL的record_queries，输出到日志
def log_record_queries():
    """
    捕获SQL的record_queries，输出到日志
    该函数需要flask app上下文环境。
    同时需要在app.config中设置SQLALCHEMY_RECORD_QUERIES = True
    只针对于flask_sqlalchemy的SQL操作有效
    """
    import flask_sqlalchemy.record_queries
    records = flask_sqlalchemy.record_queries.get_recorded_queries()
    print("records: {}".format(records))
    long_records = [r for r in records if r.duration >= long_sql_threshold]
    if long_records:
        logging.warning("".join([
            f"'sql duration: '{info.duration} 'sql location: '{info.location}\n"
            for info in long_records]))


# endregion


# region 监控，基于sqlalchemy的事件监听，自定义实现
from sqlalchemy import create_engine, event
import time


def monitor_engine(engine):
    """
    监控engine中的SQL执行，对长SQL操作输出到日志。
    """
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        context._query_start_time = time.perf_counter()

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        duration = time.perf_counter() - context._query_start_time
        if duration >= long_sql_threshold:
            logging.warning("".join(
                f"'sql duration: '{duration} 秒. 'sql statement: '{statement}.\n"
            ))

# 其他操作...
# endregion
