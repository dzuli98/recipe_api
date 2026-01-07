from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    edamam_app_id: str = Field(..., env="EDAMAM_APP_ID")
    edamam_app_key: str = Field(..., env="EDAMAM_APP_KEY")

    max_requests_per_minute: int = Field(..., env="MAX_REQUESTS_PER_MINUTE")
    window_size : int = Field(..., env="WINDOW_SIZE")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()