from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource
from pydantic_settings.sources import PydanticBaseSettingsSource

_CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


class Settings(BaseSettings):
    log_level: str = "DEBUG"
    fuzzy_match_threshold: int = 85
    fuzzy_confirm_threshold: int = 50

    model_config = SettingsConfigDict(toml_file=_CONFIG_PATH, extra="ignore")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
