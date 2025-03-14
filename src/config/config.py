from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict


env = Env()
env.read_env()


class Settings(BaseSettings):
    DEBUG: bool
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    BOT_TOKEN: str
    ADMINS: str | list[int]

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DEBUG_DB_URL(self):
        return "sqlite+aiosqlite:///tests/database.db"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
settings.ADMINS = list(map(int, env.list("ADMINS")))
