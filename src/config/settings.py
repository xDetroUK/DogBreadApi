from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pydantic import Field

class Settings(BaseSettings):
    dog_api_url: str = Field(..., alias="DOG_API_URL")
    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    log_level: str = Field("info", alias="LOG_LEVEL")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")

    model_config = ConfigDict(env_file=".env")

settings = Settings()
