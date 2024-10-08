import os
from pathlib import Path
from logging import getLogger
from py_configorm.sources.dotenv_source import DOTENVSource
from py_configorm.sources.toml_source import TOMLSource
from py_configorm.sources.json_source import JSONSource
from py_configorm.sources.yaml_source import YAMLSource
from py_configorm.sources.env_source import ENVSource
import tempfile

toml = """
    [Service]
    Host = "localhost"
    Port = 8080
    """

json = """
    {
        "Service":
        {
            "Host": "localhost",
            "Port": 8080
        }
    }
    """

yaml = """
    Service:
        Host: localhost
        Port: 8080
    """

dotenv = """
    CFGORM_SERVICE__HOST=localhost
    CFGORM_SERVICE__PORT=8080
    """

logger = getLogger("TestSources")


def test_toml_source_load():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.toml"))
    config_file.write_text(toml)

    source = TOMLSource(filepath=Path(config_file))
    config = source.load()

    logger.debug(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080


def test_json_source_load(tmp_path):
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.json"))
    config_file.write_text(json)

    source = JSONSource(filepath=Path(config_file))
    config = source.load()

    print(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080


def test_yaml_source_load(tmp_path):
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.yaml"))
    config_file.write_text(yaml)

    source = YAMLSource(filepath=Path(config_file))
    config = source.load()

    logger.info(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080


def test_env_source_load(monkeypatch):
    monkeypatch.setenv("MYAPP_SERVICE__HOST", "localhost")
    monkeypatch.setenv("MYAPP_SERVICE__PORT", "8080")

    source = ENVSource(prefix="MYAPP_")
    config = source.load()

    assert isinstance(config, dict)
    assert config["SERVICE"]["HOST"] == "localhost"
    assert config["SERVICE"]["PORT"] == "8080"


def test_dotenv_source_load(tmp_path):
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.env"))
    config_file.write_text(dotenv)

    source = DOTENVSource(filepath=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["SERVICE"]["HOST"] == "localhost"
    assert config["SERVICE"]["PORT"] == "8080"
