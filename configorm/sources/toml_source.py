"""
This module contains the TOMLSource class, a class for a TOML configuration
source.

TOML (Tom's Obvious, Minimal Language) is a minimal configuration file format
that is easy to read due to obvious semantics.

This module is part of the `configorm` package for handling configuration data.
"""

from pathlib import Path

import toml
from configorm.exception import ConfigORMError
from configorm.sources.base import SourceBase


class TOMLSource(SourceBase):
    """
    Class for a TOML configuration source.

    This class is a subclass of `SourceBase` and represents a TOML configuration
    source. It provides methods to load and save configuration data from/to a
    TOML file.

    Attributes:
        _file_path (Path): The path to the TOML configuration file.

    Methods:
        __init__(self, file_path: Path, readonly: bool = True):
            Initializes a new instance of `TOMLSource`.

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

        This method loads the configuration data from the TOML file specified
        during the initialization of this class.

        Returns:
            dict: The loaded configuration data.

        Raises:
            FileNotFoundError: If the specified TOML file does not exist.

        """
        try:
            with open(self._file_path, "r") as f:
                return toml.load(f)
        except FileNotFoundError:
            raise
        except toml.TomlDecodeError as e:
            raise ConfigORMError("Error loading TOML file: {}", format(e))

    def save(self, data: dict):
        """
        Save configuration data to this source.

        This method saves the configuration data to the TOML file specified
        during the initialization of this class. 

        Args:
            data (dict): _description_

        Raises:
            PermissionError: _description_
        """
        try:
            if self._readonly:
                raise PermissionError("This source is read-only.")

            with open(self._file_path, "w") as f:
                toml.dump(data, f)
        except FileNotFoundError:
            raise
        except toml.TomlDecodeError as e:
            raise ConfigORMError("Error saving TOML file: {}", format(e))