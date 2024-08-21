
from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn

class Settings(BaseSettings):
    connection_string: PostgresDsn = "postgresql+asyncpg://postgres:postgres@db/design_app_db"
    permit_api_key: str
    pdp_address: AnyHttpUrl = "http://localhost:7766"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "my_dev_secret"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore