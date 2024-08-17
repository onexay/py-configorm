"""
ConfigORM - A simple configuration library.

This module contains the ConfigORM class, a class for handling configuration data.

Classes:
    ConfigSchema (ConfigSchema): The ConfigSchema class.
    ConfigORM (ConfigORM): The ConfigORM class.
"""

from typing import List, Type
from pydantic import BaseModel
import pydantic

from py_configorm.exception import ConfigORMError


class ConfigSchema(BaseModel):
    """
    Base class for all user defined configuration schemas.
    """

    pass


class ConfigORM:
    def __init__(self, schema: Type[ConfigSchema], sources: List):
        self._schema = schema
        self._sources = sources
        self._config = self.load_config()

    def load_config(self) -> ConfigSchema:
        """
        Load configuration data from all the sources.

        This method loads the configuration data from all the sources specified
        during the initialization of this class. The configuration data is
        merged together and returned as a single `ConfigSchema` object.

        Returns:
            ConfigSchema: The loaded configuration data.
        """
        config_data = {}
        try:

            def merge_config(data, new_data):
                for key, value in new_data.items():
                    if isinstance(value, dict) and key in data:
                        merge_config(data[key], value)
                    else:
                        data[key] = value

            if len(self._sources) == 0:
                raise ConfigORMError("No configuration sources specified")

            for source in self._sources:
                merge_config(config_data, source.load())

            return self._schema(**config_data)
        except Exception as e:
            raise ConfigORMError("Error loading configuration data: {}", format(e))
        except pydantic.ValidationError as e:
            raise ConfigORMError("Invalid configuration data: {}", format(e))
        except TypeError as e:
            raise ConfigORMError("Invalid configuration data type: {}", format(e))

    def save_config(self):
        """
        Save configuration data to all the sources.

        This method saves the configuration data to all the sources specified
        during the initialization of this class.

        Raises:
            PermissionError: If one of the sources is read-only.
        """

        if len(self._sources) == 0:
            raise ConfigORMError("No configuration sources specified")

        for source in self._sources:
            if not source.readonly:
                source.save(self._config.model_dump())

    def reload_config(self):
        """
        Reload configuration data from all the sources.

        This method reloads the configuration data from all the sources specified
        during the initialization of this class. The configuration data is
        merged together and returned as a single `ConfigSchema` object.
        """
        self._config = self.load_config()
