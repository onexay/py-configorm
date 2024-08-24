"""
This module contains the YAMLSource class, a class for a YAML configuration
source.

This module is part of the `configorm` package for handling configuration data.
"""

from pathlib import Path
import yaml
from py_configorm.exception import ConfigORMError
from py_configorm.sources.base import BaseSource


class YAMLSource(BaseSource):
    """
    Class for a YAML configuration source.

    This class is a subclass of `SourceBase` and represents a YAML configuration
    source. It provides methods to load and save configuration data from/to a
    YAML file.

    Attributes:
        _file_path (Path): The path to the YAML configuration file.

    Methods:
        __init__(self, file_path: Path, readonly: bool = True):
            Initializes a new instance of `YAMLSource`.

        load(self) -> dict:
            Load configuration data from this source.

            Returns:
                dict: The loaded configuration data.

        save(self, data: dict):
            Save configuration data to this source.

            Args:
                data (dict): The configuration data to save.

        reload(self):
            Reload configuration data from this source.

            This method is called when the application is reloaded and the
            configuration data must be reloaded from the source.
    """

    def __init__(self, filepath: Path, readonly: bool = True):
        super().__init__(filepath, readonly)

    def load(self) -> dict:
        """
        Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        try:
            with open(self.filepath, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise e

    def save(self, data: dict):
        """
        Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        try:
            if self.readonly:
                raise PermissionError("This source is read-only.")

            with open(self.filepath, "w") as f:
                yaml.dump(data, f)
        except Exception as e:
            raise e
