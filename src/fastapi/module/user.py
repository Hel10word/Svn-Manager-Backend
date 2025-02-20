from pydantic import BaseModel


# 用户登录请求模型
class User(BaseModel):
    username: str
    password: str
