
from pydantic import BaseSettings

class Settings(BaseSettings):
    CONNECTION_STRING: str
    PERMIT_API_KEY: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "my_dev_secret"


settings = Settings()  # type: ignore