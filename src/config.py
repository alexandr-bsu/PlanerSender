from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from enum import Enum
import os

from supabase import Client as supabase

DOCKER_MODE = os.getenv("MODE")
DOTENV = os.path.join(os.path.dirname(__file__), "../.test.env")

if DOCKER_MODE == 'DEV':
    DOTENV = os.path.join(os.path.dirname(__file__), "../.prod.env")

if DOCKER_MODE == 'TEST':
    DOTENV = os.path.join(os.path.dirname(__file__), "../.test.env")


class DbSettings(BaseSettings):
    DB_HOST: str = Field(default='localhost')
    DB_USER: str = Field(default='postgres')
    DB_SECRET_KEY: str = Field(default='postgres')
    QUEUE_NAME: str = Field(default='test_send_message_telegram')

    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')


# Режимы работы приложения
class Mode(Enum):
    DEV = 'DEV'
    TEST = 'TEST'


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    mode: Mode
    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')


settings = Settings()
client = supabase(supabase_url=settings.db.DB_HOST, supabase_key=settings.db.DB_SECRET_KEY)
