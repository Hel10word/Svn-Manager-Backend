import http

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette import status
# from fastapi import HTTPException as FastHttpException
from starlette.exceptions import HTTPException as StarletteException
from starlette.responses import JSONResponse

from src.fastapi.module.response import ErrorResponse
from src.module.manager_exception import ManagerException


async def http_exception_handler(request: Request, exc: StarletteException):
    return JSONResponse(
        status_code=http.HTTPStatus(exc.status_code),
        content=ErrorResponse(code=exc.status_code, error=str(exc.detail), message="An error occurred").model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(code=422, error="Validation Error", message=str(exc)).model_dump()
    )


async def manager_exception_handler(request: Request, exc: ManagerException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(code=exc.code, error="Internal Server Error", message=exc.message).model_dump(),
    )


async def basic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(code=500, error="Internal Server Error",
                              message="An unexpected error occurred").model_dump(),
    )
