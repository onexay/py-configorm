"""
This module contains the JSONSource class, a class for a JSON configuration
source.

Attributes:
    JSONSource (JSONSource): The JSONSource class.

"""

import json
from pathlib import Path

from py_configorm.sources.base import BaseSource


class JSONSource(BaseSource):
    """A class for a JSON configuration source.

    Attributes:
        _file_path (Path): The path to the JSON configuration file.

    Methods:
        __init__(self, file_path: Path, readonly: bool = True):
            Initializes a new instance of `JSONSource`.

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

    def __init__(self, filepath: Path | None, readonly: bool = True):
        super().__init__(filepath, readonly)

    def load(self) -> dict:
        """
        Load configuration data from this source.

        This method loads the configuration data from the JSON file specified
        during the initialization of this class.

        Returns:
            dict: The loaded configuration data.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.

            json.JSONDecodeError: If there is an error decoding the JSON data.

        """
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            raise e

    def save(self, data: dict):
        """
        Save configuration data to this source.

        This method saves the configuration data to the JSON file specified
        during the initialization of this class.

        Args:
            data (dict): The configuration data to save.

        Raises:
            PermissionError: If the source is read-only.
        """
        try:
            if self.readonly:
                raise PermissionError("This source is read-only.")

            with open(self.filepath, "w") as f:
                json.dump(data, f)
        except Exception as e:
            raise e