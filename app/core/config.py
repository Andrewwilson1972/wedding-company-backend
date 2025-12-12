from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    mongo_uri: str = Field(
        default="mongodb://mongo:27017/wedding_master",
        env="MONGO_URI"
    )

    jwt_secret: str = Field(
        default="replace-this-with-a-strong-secret",
        env="JWT_SECRET"
    )
    jwt_algorithm: str = Field(
        default="HS256",
        env="JWT_ALGORITHM"
    )
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    app_name: str = Field(default="wedding-backend", env="APP_NAME")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")

    # pydantic v2 / pydantic-settings config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

# Create global settings instance
settings = Settings()
