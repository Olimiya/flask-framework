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
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# region 监控实现
# 设置
debug = False  # 是否开启debug模式
long_sql_threshold = 0.0001  # 长SQL阈值，单位秒

if debug:
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy(app)


# 捕获SQL的record_queries，输出到日志
def log_record_queries(app):
    import flask_sqlalchemy.record_queries
    records = flask_sqlalchemy.record_queries.get_recorded_queries()
    long_records = [r for r in records if r.duration >= long_sql_threshold]
    if long_records:
        logging.warning("".join([
            f"'info.duration: '{info.duration} 'info.location: '{info.location}\n"
            for info in long_records]))


# region 测试
# 表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String)


with app.app_context():
    db.create_all()


# 执行创建，生成大量虚拟数据，形成秒级别的操作延迟
@app.route('/create')
def create():
    for i in range(1000):
        user = User(username='user' + str(i), email='user' + str(i) + '@example.com')
        db.session.add(user)
    db.session.commit()
    log_record_queries(app)
    return 'ok'


# 长SQL测试，执行一个慢SQL的操作
@app.route('/long_sql')
def long_sql():
    # 查询所有用户，返回
    users = User.query.all()
    log_record_queries(app)
    return jsonify([user.username for user in users])


# run
if __name__ == '__main__':
    app.run(debug=True)

# endregion
