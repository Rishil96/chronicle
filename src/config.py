from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo


class Settings(BaseSettings):
    db_driver: str
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    daily_updates_days: int
    project_log_days: int
    recency_hours: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        if self.db_driver == "sqlite":
            return f"sqlite:///{self.db_name}.db"
        elif self.db_driver == "postgresql":
            return f"postgresql+psycopg2://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        elif self.db_driver == "mssql":
            return f"mssql+pyodbc://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?driver=ODBC+Driver+17+for+SQL+Server"
        raise ValueError(f"Unsupported database driver: {self.db_driver}")


# Global variables to be used across the project
settings = Settings()   # noqa
# IST Timezone
IST = ZoneInfo("Asia/Kolkata")
