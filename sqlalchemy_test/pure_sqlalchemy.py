# -*- coding: utf-8 -*-
# @Time: 2023/5/19 9:16
# @Author: lijunhui
# @File: pure_sqlalchemy.py
"""
pure_sqlalchemy.py
纯sqlalchemy实现
"""
import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String

# region 创建数据库连接
# 创建数据库连接
engine = create_engine('sqlite:///SQLAlchemy.db')
# 创建Session
Session = sessionmaker(bind=engine)
session = Session()
# endregion

# region 创建表
# 创建表
# Base = sqlalchemy.orm.declarative_base()
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     age = Column(Integer)
#     email = Column(String(120))
#
#     def __repr__(self):
#         return "<User(name='%s', age='%d', email='%s')>" % (self.name, self.age, self.email)
#
#
# Base.metadata.create_all(engine)
# endregion

# region CURD
# 插入数据
# new_user = User(name='John Doe', age=30, email='john@example.com')
# session.add(new_user)
#
# session.commit()
#
# # 查询数据
# users = session.query(User).filter_by(age=30)
#
# for user in users:
#     print(user)
#
# # 更新数据
# userToUpdate = session.query(User).filter_by(name='John Doe').first()
# userToUpdate.age = 35
#
# session.commit()

# 删除数据
# userToDelete = session.query(User).filter_by(name='John Doe').one()
# session.delete(userToDelete)
#
# session.commit()

# endregion

# region pandas使用
# import pandas as pd
# from watch_long_sql import log_record_queries
#
# # 使用sql requery，# 没有flask app上下文，无法使用
# df = pd.read_sql_query("SELECT * FROM users", engine)
# print("query: \n")
# print(df)


# endregion


# region profiling，信息太多了

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import cProfile
import pstats


# 定义查询函数
def query_function():
    # 创建连接
    conn = engine.connect()

    # 执行查询
    result = conn.execute(text('SELECT * FROM users'))

    # 打印查询结果
    for row in result:
        print(row)

    # 关闭连接
    conn.close()


# 使用cProfile运行查询函数，并保存结果到stats变量中
# pr = cProfile.Profile()
# pr.enable()
# query_function()
# pr.disable()
# stats = pstats.Stats(pr)
#
# # 根据cumulative时间排序查询语句，并打印
# stats.sort_stats('cumulative').print_stats()

# endregion

