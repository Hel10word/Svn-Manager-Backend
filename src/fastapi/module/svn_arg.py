from pydantic import BaseModel


# Svn 请求操作参数
class SvnArg(BaseModel):
    paths: list[str] = []
    comment: str = ""
