from urllib.parse import unquote

from fastapi import APIRouter, Depends, status, Request
from starlette.exceptions import HTTPException

from src.fastapi.api.login_api import router as login_router
from src.fastapi.api.logout_api import router as logout_router
from src.fastapi.api.svn_api import router as svn_router
from src.manager.caches_manager import CacheManager
from src.manager.config_manager import ConfigManager
from src.manager.log_manager import LogManager
from src.module.config.config_enum import ConfigEnum
from src.util.token_util import TokenUtil


# Token 校验 过滤器
def verify_token_filter(request: Request):
    # 获取 Token
    # token = request.headers.get('Authorization')
    token = request.cookies.get(fastapiConfig.cookieKey)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    # 验证并更新缓存 Token
    try:
        payload = TokenUtil.decoded_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        username = TokenUtil.get_username(payload=payload)
        exp = TokenUtil.get_exp(payload=payload)
        cacheToken = cacheManager.get_user_token(username)
        if not cacheToken:
            cacheManager.set_user_token(username, token)
        else:
            cacheExp = TokenUtil.get_exp(token=cacheToken)
            if exp < cacheExp:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Account already logged in elsewhere")
            elif exp > cacheExp:
                cacheManager.set_user_token(username, token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    # 设置缓存上下文
    cacheManager.set_context_user(username)


# 日志记录 过滤器
async def print_log_filter(request: Request):
    user = cacheManager.get_context_user()
    body = await request.body()
    query_params = unquote(str(request.query_params))
    headers = request.headers

    logger.info(
        # f"Request path: {request.url.path}, "
        # f"Method: {request.method}, "
        f"{user.username} "
        f"{request.method} : {request.url.path} "
        f"Query params: {query_params}, "
        # f"Headers: {headers}, "
        f"Body: {body.decode() if body else '{}'}"
    )


router = APIRouter()
logger = LogManager.get_logger(__name__)
cacheManager = CacheManager()
fastapiConfig = ConfigManager.get(ConfigEnum.ENV).fastapi

# 将其他路由模块挂载到主路由上
router.include_router(svn_router, tags=["SVN"], dependencies=[Depends(verify_token_filter), Depends(print_log_filter)])
router.include_router(logout_router, tags=["LOGOUT"], dependencies=[Depends(verify_token_filter),
                                                                    Depends(print_log_filter)])
router.include_router(login_router, tags=["Authentication"])
