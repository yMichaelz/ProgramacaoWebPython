from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    app_env: str = "production"
    app_secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
