import os
from pydantic import BaseSettings


class Settings(BaseSettings):

    ENV: str
    SERVICE_NAME: str
    SERVICE_VERSION: str
    DATABASE_URI: str

    DEFAULT_PAGE_SIZE: int
    CORS_ALLOWED_ORIGINS: str
    ADMIN_ROLE_ID: str
    RESOURCE_NAME: str = "item/"

    USER_MANAGEMENT_URL: str = "not set up yet"


class ProdConfig(Settings):
    pass


class DevConfig(Settings):
    class Config:
        env_file = "./config/dev.env"


def get_conf():
    if os.getenv("ENV"):
        return ProdConfig()
    else:
        return DevConfig()


conf = get_conf()

if __name__ == "__main__":
    print(conf)
