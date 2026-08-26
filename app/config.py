from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM : str
    EXPIRATION_TIME : int  
    DB_HOSTNAME : str
    DB_PORT : str
    DB_PASSWORD : str
    DB_NAME : str
    DB_USERNAME : str 

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()