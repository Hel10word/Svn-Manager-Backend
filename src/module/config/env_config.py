from pydantic import BaseModel


class FastApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    cookieKey: str = "access_token"


class EnvConfig(BaseModel):
    baseSvnUrl: str = "https://svn.wedobest.com.cn/svn/pdragon"
    basePath: str = ""
    defUsername: str = ""
    defPassword: str = ""
    fastapi: FastApiConfig
