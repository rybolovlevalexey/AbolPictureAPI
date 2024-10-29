from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.split(os.path.split(
        os.path.normpath(os.path.abspath(__file__)))[0])[0], ".env"))

    def get_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()
