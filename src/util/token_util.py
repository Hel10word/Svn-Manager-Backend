from datetime import datetime, timedelta
from typing import Any

import jwt

from src.manager.log_manager import LogManager

logger = LogManager.get_logger(__name__)

SECRET_KEY = 'svn-manager-secret-key'


class TokenUtil:

    @staticmethod
    def generate_token(username) -> str:
        user_info = {'sub': username}
        to_encode = user_info.copy()
        expire = datetime.utcnow() + timedelta(minutes=360)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decoded_token(token) -> Any:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Token expired: {e}")  # 打印 token 过期错误信息
        except jwt.DecodeError as e:
            logger.error(f"Token decode error: {e}")  # 打印 token 格式错误信息
        except Exception as e:
            logger.exception("Unexpected error decoding token")  # 打印任何其他异常
        return None

    @staticmethod
    def verify_token(token) -> bool:
        if TokenUtil.decoded_token(token):
            return True
        else:
            return False

    @staticmethod
    def get_payload_value(key: str = None, token: str = None, payload: Any = None) -> str | None:
        if token:
            payload = TokenUtil.decoded_token(token)
        if payload:
            return payload.get(key)
        return None

    @staticmethod
    def get_username(token: str = None, payload: Any = None) -> str | None:
        return TokenUtil.get_payload_value('sub', token=token, payload=payload)

    @staticmethod
    def get_exp(token: str = None, payload: Any = None) -> str | None:
        return TokenUtil.get_payload_value('exp', token=token, payload=payload)
