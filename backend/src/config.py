from decouple import config
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    db_url: str = config(
        "DATABASE_URL", default="postgresql://user:password@localhost/jano"
    )
    secret_key: str = config("SECRET_KEY")

    @classmethod
    def generate(cls):
        return AppSettings()


settings = AppSettings.generate()
