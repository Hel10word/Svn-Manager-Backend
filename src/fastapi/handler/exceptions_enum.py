from enum import Enum
from typing import Callable, Union, Type

from src.fastapi.handler.exception_handlers import *


class ExceptionHandlers(Enum):
    # 如果 code 匹配 优先处理 code ; 其次再按照 Exception Type 匹配

    # Http.status_code handler
    # CODE_401 = (401, http_exception_handler)
    # CODE_403 = (403, http_exception_handler)
    # Exception handler
    # FAST_HTTP_ERROR = (FastHttpException, http_exception_handler)
    HTTP_ERROR = (StarletteException, http_exception_handler)
    VALIDATION_ERROR = (RequestValidationError, validation_exception_handler)
    MANAGER_ERROR = (ManagerException, manager_exception_handler)
    BASIC_ERROR = (Exception, basic_exception_handler)

    def __init__(self, exc_type: Union[int, Type[Exception]], handler: Callable):
        self.exc_type = exc_type
        self.handler = handler
