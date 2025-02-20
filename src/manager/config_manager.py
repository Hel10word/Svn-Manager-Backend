import os
from typing import cast

import yaml

from src.module.config.config_enum import ConfigEnum


class ConfigManager:
    _instance = None
    _configs = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # 当实例不存在时，创建它并调用私有 load 方法
            cls._instance._load()
        return cls._instance

    def _load(self):
        for config_enum in ConfigEnum:
            file_path = os.path.join('config', config_enum.file)
            with open(file_path, 'r', encoding='utf-8') as yml_file:
                # 读取配置文件内容并将其转换为字典
                config_data = yaml.safe_load(yml_file)

            # 将创建的对象存储起来
            self._configs[config_enum.name()] = config_enum.obj(**config_data)
        print("Configurations loaded.")

    @staticmethod
    def get(config_enum: ConfigEnum = None):
        instance = ConfigManager()  # 确保有实例存在并且已经初始化
        # return instance._configs.get(config_enum.name())
        return cast(config_enum.obj, instance._configs.get(config_enum.name()))

    @staticmethod
    def reload():
        instance = ConfigManager()  # 确保有实例存在并且已经初始化
        instance._load()
        print("Configurations reloaded.")
