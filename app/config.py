from pydantic_settings import BaseSettings, SettingsConfigDict

# Pydantic will validate these for us
# "loc" is the default variable for DATABASE_PASSWORD
class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
# Access variable DATABASE_PASSWORD by 
# settings.DATABASE_PASSWORD 