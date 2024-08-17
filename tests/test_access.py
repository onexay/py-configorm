import os
from pathlib import Path
from logging import getLogger

import pytest
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

toml_modified = \
    """
    [Service]
    Host = "localhost"
    Port = 4000
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

json_modified = \
    """
    {
        "Service":
        {
            "Host": "localhost",
            "Port": 4000
        }
    }
    """

yaml = """
    Service:
        Host: localhost
        Port: 8080
    """

yaml_modified = \
    """
    Service:
        Host: localhost
        Port: 4000
    """

dotenv = """
    CFGORM_Service__Host=localhost
    CFGORM_Service__Port=8080
    """

dotenv_modified = \
    """
    CFGORM_Service__Host=localhost
    CFGORM_Service__Port=4000
    """

logger = getLogger("TestSources")


def test_toml_source_ro():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.toml"))
    config_file.write_text(toml)

    source = TOMLSource(file_path=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    with pytest.raises(PermissionError):
        source.save(config)

def test_toml_source_rw():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.toml"))
    config_file.write_text(toml)

    source = TOMLSource(file_path=Path(config_file), readonly=False)
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    source.save(config)

    source = TOMLSource(file_path=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 4000

def test_json_source_ro():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.json"))
    config_file.write_text(json)

    source = JSONSource(file_path=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    with pytest.raises(PermissionError):
        source.save(config)

def test_json_source_rw():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.json"))
    config_file.write_text(json)

    source = JSONSource(file_path=Path(config_file), readonly=False)
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    source.save(config)

    source = JSONSource(file_path=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 4000

def test_yaml_source_ro():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.yaml"))
    config_file.write_text(yaml)

    source = YAMLSource(file_path=Path(config_file))
    config = source.load()

    logger.info(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    with pytest.raises(PermissionError):
        source.save(config)

def test_yaml_source_rw():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.yaml"))
    config_file.write_text(yaml)

    source = YAMLSource(file_path=Path(config_file), readonly=False)
    config = source.load()

    logger.info(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 8080

    config["Service"]["Port"] = 4000
    source.save(config)

    source = YAMLSource(file_path=Path(config_file))
    config = source.load()

    logger.info(config)

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == 4000

def test_env_source_ro(monkeypatch):
    monkeypatch.setenv("MYAPP_SERVICE__HOST", "localhost")
    monkeypatch.setenv("MYAPP_SERVICE__PORT", "8080")

    source = ENVSource(prefix="MYAPP_")
    config = source.load()

    assert isinstance(config, dict)
    assert config["SERVICE"]["HOST"] == "localhost"
    assert config["SERVICE"]["PORT"] == "8080"

    config["PORT"] = 4000
    with pytest.raises(PermissionError):
        source.save(config)

def test_env_source_rw(monkeypatch):
    monkeypatch.setenv("MYAPP_SERVICE__HOST", "localhost")
    monkeypatch.setenv("MYAPP_SERVICE__PORT", "8080")

    source = ENVSource(prefix="MYAPP_", readonly=False)
    config = source.load()

    assert isinstance(config, dict)
    assert config["SERVICE"]["HOST"] == "localhost"
    assert config["SERVICE"]["PORT"] == "8080"

    config["SERVICE"]["PORT"] = "4000"
    source.save(config)

    source = ENVSource(prefix="MYAPP_")
    config = source.load()

    assert isinstance(config, dict)
    assert config["SERVICE"]["HOST"] == "localhost"
    assert config["SERVICE"]["PORT"] == "4000"

def test_dotenv_source_ro():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.env"))
    config_file.write_text(dotenv)

    source = DOTENVSource(file_path=Path(config_file))
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == "8080"

    config["CFGORM_SERVICE__PORT"] = 4000
    with pytest.raises(PermissionError):
        source.save(config)

def test_dotenv_source_rw():
    config_file = Path(os.path.join(tempfile.mkdtemp(), "config.env"))
    config_file.write_text(dotenv)

    source = DOTENVSource(file_path=Path(config_file), readonly=False)
    config = source.load()

    assert isinstance(config, dict)
    assert config["Service"]["Host"] == "localhost"
    assert config["Service"]["Port"] == "8080"

    config["CFGORM_SERVICE__PORT"] = "4000"
    with pytest.raises(NotImplementedError):
        source.save(config)