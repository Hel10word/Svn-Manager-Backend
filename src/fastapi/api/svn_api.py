from fastapi import APIRouter
from starlette_context import context

from src.fastapi.module.response import StandardResponse
from src.fastapi.module.svn_arg import SvnArg
from src.util.svn_util import SvnUtil

router = APIRouter(prefix="/svn")


@router.get("/svn-data/", response_model=StandardResponse)
async def svn_data(path: str):
    user = context.get('user')
    data = SvnUtil.list_locked_files(path, user.username, user.password)
    return StandardResponse(code=200, data=data)


@router.post("/svn-lock/", response_model=StandardResponse)
async def svn_lock(svnArg: SvnArg):
    user = context.get('user')
    success, failed = SvnUtil.lock_files(svnArg.paths, user.username, user.password, svnArg.comment)
    return StandardResponse(code=200, data={"success": success, "failed": failed})


@router.post("/svn-unlock/", response_model=StandardResponse)
async def svn_unlock(svnArg: SvnArg):
    user = context.get('user')
    success, failed = SvnUtil.unlock_files(svnArg.paths, user.username, user.password)
    return StandardResponse(code=200, data={"success": success, "failed": failed})


@router.post("/svn-log/", response_model=StandardResponse)
async def svn_log(svnArg: SvnArg):
    user = context.get('user')
    logObjects = SvnUtil.view_logs(svnArg.paths, user.username, user.password)
    return StandardResponse(code=200, data=list(logObjects.values()))
