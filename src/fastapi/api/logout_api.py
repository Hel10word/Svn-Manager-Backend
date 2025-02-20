from fastapi import APIRouter, Response

from src.fastapi.module.response import StandardResponse
from src.manager.caches_manager import CacheManager
from src.manager.config_manager import ConfigManager
from src.manager.log_manager import LogManager
from src.module.config.config_enum import ConfigEnum

router = APIRouter()
cacheManager = CacheManager()
logger = LogManager.get_logger(__name__)
envConfig = ConfigManager.get(ConfigEnum.ENV)
fastapiConfig = envConfig.fastapi


# 登出
@router.post("/logout", response_model=StandardResponse)
async def logout(response: Response):
    user = cacheManager.get_context_user()
    if user:
        # 清除 缓存
        cacheManager.remove_user_cache(user.username)
    # 清除 Cookie
    response.delete_cookie(key=fastapiConfig.cookieKey)
    logger.info(f"user logout => {user.username} logout OK .")
    return StandardResponse(data="logout success!!")
