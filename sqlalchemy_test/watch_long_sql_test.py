import pandas as pd
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# region 基于flask_sqlalchemy的测试
# from sqlalchemy_test.watch_long_sql import debug, log_record_queries
#
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# if debug:
#     app.config["SQLALCHEMY_RECORD_QUERIES"] = True
#     logging.basicConfig(level=logging.DEBUG)
#
# db = SQLAlchemy(app)
#
#
# # 表
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False)
#     email = db.Column(db.String)
#
#
# with app.app_context():
#     db.create_all()
#
#
# # 执行创建，生成大量虚拟数据，形成秒级别的操作延迟
# @app.route('/create')
# def create():
#     for i in range(1000):
#         user = User(username='user' + str(i), email='user' + str(i) + '@example.com')
#         db.session.add(user)
#     db.session.commit()
#     log_record_queries()
#     return 'ok'
#
#
# # 长SQL测试，执行一个慢SQL的操作
# @app.route('/long_sql')
# def long_sql():
#     # 查询所有用户，基于SQL语句查询
#     users = db.session.execute(text('SELECT * FROM user'))
#     log_record_queries()
#     return jsonify([user.username for user in users])


# endregion


# region 基于sqlalchemy的测试
from db_connect import test_conn
# flask sqlalchemy 绑定要监听的engine
import flask_sqlalchemy.record_queries


# flask_sqlalchemy.record_queries._listen(engine)


# 测试alchemy
@app.route('/db')
def alchemy():
    with test_conn.connect() as conn:
        users = conn.execute(text('SELECT * FROM user'))
        return jsonify([user.id for user in users])


# 测试pandas
@app.route('/')
def index():
    df = pd.read_sql_query("SELECT * FROM user", test_conn)
    print("query: \n")
    print(df)
    return "Hello, World!"


# endregion


# run
if __name__ == '__main__':
    app.run(debug=True)
