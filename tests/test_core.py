import os
from pathlib import Path
import tempfile

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn
from pydantic_core import MultiHostUrl, Url
import pytest
from py_configorm.core import ConfigORM, ConfigSchema
from py_configorm.sources.dotenv_source import DOTENVSource
from py_configorm.sources.json_source import JSONSource
from py_configorm.sources.toml_source import TOMLSource

toml = """
    [Service]
    Host = "localhost"
    Port = 8080
    """

json = """
    {
        "Service": {
            "Port": 18080
        },
        "Store": {
            "Url": "postgresql://localhost:5432/store",
            "Debug": true,
            "ConnectionPoolDebug": true
        }
    }
    """

dotenv = """
    CFGORM_Cache__Url="redis://localhost:6379/0"
    """


class ServiceConfigTest(BaseModel):
    Host: str = Field(..., description="Host running the service")
    Port: int = Field(..., description="Port bound to the service")


class StoreConfigTest(BaseModel):
    Url: PostgresDsn = Field(..., description="URL of the database")
    Debug: bool = Field(..., description="Enable debug mode")
    ConnectionPoolDebug: bool = Field(
        ..., description="Enable connection pool debug mode"
    )


class CacheConfigTest(BaseModel):
    Url: RedisDsn = Field(..., description="URL of the cache")


class ConfigTest(ConfigSchema):
    Service: ServiceConfigTest = Field(..., description="Service configuration")
    Store: StoreConfigTest = Field(..., description="Store configuration")
    Cache: CacheConfigTest = Field(..., description="Cache configuration")


def test_valid_config_load():
    config_file_toml = Path(os.path.join(tempfile.mkdtemp(), "config.toml"))
    config_file_toml.write_text(toml)

    config_file_json = Path(os.path.join(tempfile.mkdtemp(), "config.json"))
    config_file_json.write_text(json)

    config_file_dotenv = Path(os.path.join(tempfile.mkdtemp(), "config.env"))
    config_file_dotenv.write_text(dotenv)

    toml_source = TOMLSource(filepath=Path(config_file_toml))
    json_source = JSONSource(filepath=Path(config_file_json))
    dotenv_source = DOTENVSource(filepath=Path(config_file_dotenv))

    cfg_orm = ConfigORM(
        schema=ConfigTest, sources=[toml_source, json_source, dotenv_source]
    )

    cfg: ConfigTest = cfg_orm.load()

    assert isinstance(cfg, ConfigTest)

    assert cfg.Service.Host == "localhost"
    assert cfg.Service.Port == 18080
    assert cfg.Store.Url == MultiHostUrl("postgresql://localhost:5432/store")
    assert cfg.Store.Debug is True
    assert cfg.Store.ConnectionPoolDebug is True
    assert cfg.Cache.Url == Url("redis://localhost:6379/0")


def test_invalid_config_load():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.json"))
    config_file.write_text(json)

    json_source = JSONSource(filepath=Path(config_file))

    with pytest.raises(Exception):
        cfg_orm = ConfigORM(schema=ConfigTest, sources=[json_source])
        cfg: ConfigTest = cfg_orm.load()
