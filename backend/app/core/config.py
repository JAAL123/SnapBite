from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GOOGLE_API_KEY: str    

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        )


settings = Settings()
