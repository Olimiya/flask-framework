# -*- coding: utf-8 -*-
# @Time: 2023/5/19 17:00
# @Author: lijunhui
# @File: autoswagger.py
"""
autoswagger.py
"""
from flask import Flask
from flask_restx  import Api, Resource

app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """返回Hello World"""
        return {'message': 'Hello World'}


if __name__ == '__main__':
    app.run(debug=True)
