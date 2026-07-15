

from pydantic_settings import BaseSettings, SettingsConfigDict





# shared settings parameters for the app.

class EnvSettings(BaseSettings):
    # Do not use spaces inside .env, may cause problems when reading
    ENV_MODE:str = "dev"
    DATA_VALIDATION_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_PORT: int
    REDIS_HOST: str = 'localhost'


    # # old style, deprecated
    # class Config:
    #     env_file = ".env"


    model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8"
        )