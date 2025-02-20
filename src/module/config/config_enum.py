from enum import Enum
from typing import Type

from src.module.config.env_config import EnvConfig


class ConfigEnum(Enum):
    ENV = ('env.yaml', EnvConfig)

    def __init__(self, file: str, obj: Type):
        self.file = file
        self.obj = obj

    def name(self) -> str:
        return self.__str__()
