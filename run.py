import logging

import uvicorn
from fastapi import FastAPI
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware
from fastapi.middleware.cors import CORSMiddleware

from src.fastapi.handler.exceptions_enum import ExceptionHandlers
from src.fastapi.routers import router as api_router
from src.manager.config_manager import ConfigManager
from src.module.config.config_enum import ConfigEnum


# 启动 FastAPI
def init_fastapi():
    # 注入异常处理
    app = FastAPI(exception_handlers={exc_handler.exc_type: exc_handler.handler for exc_handler in ExceptionHandlers})
    # 引入 starlette-context 中的插件和中间件来为每一个请求设置一个上下文
    app.add_middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            plugins.UserAgentPlugin(),
        )
    )
    # 引入 异常捕获中间件
    # exception_handlers_dict = {exc_handler.exc_type: exc_handler.handler for exc_handler in ExceptionHandlers}
    # app.add_middleware(
    #     ExceptionMiddleware,
    #     handlers=exception_handlers_dict
    # )
    # for exc_handler in ExceptionHandlers:
    #     app.add_exception_handler(exc_handler.exc_type, exc_handler.handler)
    # app.add_exception_handler()
    #
    # app.exception_handler(dict)

    # 设置 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[f"http://{envConfig.fastapi.host}:{envConfig.fastapi.port}"],  # 您的前端应用的地址
        allow_origins=["*"],  # 您的前端应用的地址
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有头
    )
    # 注册路由
    app.include_router(api_router)

    # 启动项目
    uvicorn.run(app, host=envConfig.fastapi.host, port=envConfig.fastapi.port, log_level="info")
    pass


# 设置日志默认打印的等级
logging.basicConfig(level=logging.INFO)
# 加载 默认配置文件
envConfig = ConfigManager.get(ConfigEnum.ENV)
if __name__ == '__main__':
    init_fastapi()
