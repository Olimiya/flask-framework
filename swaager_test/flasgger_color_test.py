# -*- coding: utf-8 -*-
# @Time: 2023/5/19 16:25
# @Author: lijunhui
# @File: color_test.py
"""
color_test.py
"""
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/colors/<palette>/')
def colors(palette):
    """示例端点按调色板返回颜色列表
    这是使用文档字符串作为spec。
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: 颜色列表（可被调色板过滤）
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    all_colors = {
        'cmyk': ['cyan', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)


app.run(debug=True)
