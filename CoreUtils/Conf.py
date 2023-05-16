# -*- coding: utf-8 -*-
# @Time: 2023/5/16 9:43
# @Author: lijunhui
# @File: Conf.py
"""
Conf.py
"""
import importlib
import typing


class Conf():
    def __init__(self, module_name: str, blueprint_name: str,
                 is_verify_token: bool = False, verify_func: typing.Callable = None):
        self.module_name = module_name
        self.blueprint_name = blueprint_name
        self.is_verify_token = is_verify_token
        self.verify_func = verify_func

    # get获取各个属性
    def get_module_name(self):
        return self.module_name

    def get_blueprint_name(self):
        return self.blueprint_name

    def get_is_verify_token(self):
        return self.is_verify_token

    def get_verify_func(self):
        return self.verify_func


class BluePrintConfig:
    def __init__(self, config: Conf):
        self.config = config

    def get_module_name(self):
        return self.config.get_module_name()

    def get_blueprint_name(self):
        return self.config.get_blueprint_name()

    # 根据配置信息，加载module
    def get_module(self):
        module_name = self.get_module_name()
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise
        return module

    def get_blueprint(self):
        blueprint_name = self.get_blueprint_name()
        module = self.get_module()
        try:
            blueprint = getattr(module, blueprint_name)
        except AttributeError:
            raise
        return blueprint


# URL定义，包含prefix、module名称、蓝图名称等
class UrlDefine(BluePrintConfig):
    def __init__(self, prefix, config: Conf):
        super().__init__(config)
        self.prefix = prefix

    # get获取各个属性
    def get_prefix(self):
        return self.prefix


# 蓝图定义，包含蓝图名称、是否需要token验证、token验证函数
class BluePrintDefine(BluePrintConfig):

    def get_is_verify_token(self):
        return self.config.get_is_verify_token()

    def get_verify_func(self):
        return self.config.get_verify_func()
