from typing import Any, Optional

from pydantic import BaseModel


class StandardResponse(BaseModel):
    code: int = 200
    data: Any
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    code: int
    error: str
    message: Optional[str]
