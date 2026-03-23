import os
import sys
from pathlib import Path
from typing import Literal

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def _is_testing() -> bool:
    if os.environ.get("TESTING"):
        return True
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return True
    return "pytest" in sys.modules


def _get_env_file() -> str:
    testing_env = Path(__file__).resolve().parent.parent.parent / ".env.testing"
    if _is_testing() and testing_env.is_file():
        return str(testing_env)
    return ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_get_env_file(),
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str

    # @demo-code default value example
    SECRET_KEY: str = "secretkey"

    # @demo-code computed field example
    @computed_field  # type: ignore[prop-decorator]
    @property
    def project_display_name(self) -> str:
        return f"{self.PROJECT_NAME} ({self.ENVIRONMENT})"

    # @demo-code after validation example
    @model_validator(mode="after")
    def check_secret(self) -> Self:
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == "secretkey":
            raise ValueError("SECRET_KEY cannot be default in production")
        return self


settings = Settings()  # type: ignore[call-arg]
