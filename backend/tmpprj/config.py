from urllib.parse import quote_plus

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    sql_addr: str = "localhost"
    sql_port: int = 3306

    sql_user: str = Field(default="dbtmp", validation_alias=AliasChoices("SQL_USER", "DB_USER"))
    sql_password: str = Field(validation_alias=AliasChoices("SQL_PASSWORD", "DB_PASSWORD"))
    sql_db: str = Field(default="dbtmp", validation_alias=AliasChoices("SQL_DB", "DB_NAME"))

    passwd_salt: str

    @property
    def database_uri(self) -> str:
        return (
            f"mysql+pymysql://{self.sql_user}:{quote_plus(self.sql_password)}"
            f"@{self.sql_addr}:{self.sql_port}/{self.sql_db}"
        )


settings = Settings()
