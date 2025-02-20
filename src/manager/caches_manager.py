from starlette_context import context

from src.fastapi.module.user import User
from src.util.token_util import TokenUtil

"""
因为懒 没有 使用缓存中间件 或则 数据库
简单实现了 内部缓存逻辑
"""


class CacheManager:
    _instance = None
    __user_caches = {}
    __token_caches = {}
    __CONTEXT_USER_KEY = "user"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
        return cls._instance

    def set_context_user(self, username: str):
        if username in self.__user_caches.keys():
            user = self.__user_caches.get(username)
        else:
            user = User(username=username, password="")
        context[self.__CONTEXT_USER_KEY] = user

    def get_context_user(self) -> User:
        return context.get(self.__CONTEXT_USER_KEY)

    def remove_user_cache(self, username: str):
        self.__token_caches[username] = None
        self.__user_caches[username] = None

    def get_user_token(self, username: str):
        return self.__token_caches.get(username)

    def set_user_token(self, username: str, token: str):
        self.__token_caches[username] = token

    def generate_user_cache(self, user: User, token: str) -> bool:
        """
        尝试手动实现 缓存功能
        """
        username = TokenUtil.get_username(token=token)
        # 是否是同一个用户
        if user.username != username:
            return False
        self.__token_caches[username] = token
        self.__user_caches[username] = user
        return True
