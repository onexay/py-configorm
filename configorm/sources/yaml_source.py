"""
This module contains the YAMLSource class, a class for a YAML configuration
source.

This module is part of the `configorm` package for handling configuration data.
"""

from pathlib import Path
import yaml
from configorm.exception import ConfigORMError
from configorm.sources.base import SourceBase


class YAMLSource(SourceBase):
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

    def __init__(self, file_path: Path, readonly: bool = True):
        super().__init__(readonly)
        self._file_path = file_path

    def load(self) -> dict:
        """
        Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        try:
            with open(self._file_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise
        except yaml.YAMLError as e:
            raise ConfigORMError("Error loading YAML file: {}", format(e))

    def save(self, data: dict):
        """
        Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        try:
            if self.readonly:
                raise PermissionError("This source is read-only.")
            
            with open(self._file_path, "w") as f:
                yaml.dump(data, f)
        except (FileNotFoundError, PermissionError):
            raise
