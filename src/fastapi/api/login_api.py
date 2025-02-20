from fastapi import APIRouter, HTTPException, status, Response

from src.fastapi.module.response import StandardResponse
from src.fastapi.module.user import User
from src.manager.caches_manager import CacheManager
from src.manager.config_manager import ConfigManager
from src.manager.log_manager import LogManager
from src.module.config.config_enum import ConfigEnum
from src.util.svn_util import SvnUtil
from src.util.token_util import TokenUtil

router = APIRouter()
cacheManager = CacheManager()
logger = LogManager.get_logger(__name__)
envConfig = ConfigManager.get(ConfigEnum.ENV)
fastapiConfig = envConfig.fastapi


# 登录
@router.post("/login", response_model=StandardResponse)
async def login(user: User, response: Response):
    logger.info(f"user login => username : {user.username}")
    # 校验账号密码
    if not SvnUtil.check_connection(user.username, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名密码错误")
    token = TokenUtil.generate_token(user.username)
    # logger.info(f"user login => generate token OK , token : {token}")
    response.set_cookie(key=fastapiConfig.cookieKey, value=f"{token}", httponly=True)  # 设置 HttpOnly Cookie
    logger.info(f"user login => set cookie OK , token : {token}")
    # 设置缓存对象
    cacheManager.generate_user_cache(user=user, token=token)
    logger.info(f"user login => generate cache OK , username : {user.username}")
    # 此处应生成并返回JWT token
    # return StandardResponse(data={"access_token": token, "token_type": "Authorization"})
    return StandardResponse(data={"username": user.username, "path": envConfig.basePath})
