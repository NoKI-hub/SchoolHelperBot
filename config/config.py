from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: str
    ADMINS: list[int]

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}:{self.DB_NAME}@{self.DB_HOST}:{self.DB_PORT}/sa"

    model_config = SettingsConfigDict(env_file=".env")
env = Env()
env.read_env()

settings = Settings()
