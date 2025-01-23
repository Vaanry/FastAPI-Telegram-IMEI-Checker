from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    database_url: str
    secret_key: str
    algorithm: str
    token: str
    api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
