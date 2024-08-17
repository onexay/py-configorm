"""
ConfigORM - A simple configuration library.

This module contains the DOTENVSource class, a class for a dotenv configuration
source.

Attributes:
    DOTENVSource (DOTENVSource): The DOTENVSource class.

"""

from pathlib import Path

import dotenv

from py_configorm.sources.base import SourceBase


class DOTENVSource(SourceBase):
    """Class for a dotenv configuration source.

    This class is a subclass of `SourceBase` and represents a dotenv
    configuration source. It provides methods to load and save configuration
    data from/to a dotenv file.

    Attributes:
        _file_path (Path): The path to the dotenv configuration file.

    Methods:
        __init__(self, file_path: Path, readonly: bool = True):
            Initializes a new instance of `DOTENVSource`.

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

    def __init__(
        self,
        file_path: Path,
        prefix: str = "CFGORM_",
        readonly: bool = True,
        nesting_slug: str = "__",
    ):
        super().__init__(readonly)
        self._file_path = file_path
        self._prefix = prefix
        self._nesting_slug = nesting_slug

    def load(self) -> dict:
        """Load configuration data from this source.

        This method loads the configuration data from the dotenv file specified
        during the initialization of this class.

        Returns:
            dict: The loaded configuration data.

        Raises:
            FileNotFoundError: If the specified dotenv file does not exist.
        """
        try:
            data = {}
            with open(self._file_path, "r") as f:
                vars_ = dotenv.dotenv_values(dotenv_path=f.name)
                for key, value in vars_.items():
                    n_key = key.split(self._prefix, maxsplit=1)[1]
                    l1_keys = n_key.split(self._nesting_slug, maxsplit=1)
                    if l1_keys[0] in data:
                        if l1_keys[1] in data[l1_keys[0]]:
                            data[l1_keys[0]][l1_keys[1]] = value
                        else:
                            data[l1_keys[0]][l1_keys[1]] = {}
                            data[l1_keys[0]][l1_keys[1]] = value
                    else:
                        data[l1_keys[0]] = {}
                        data[l1_keys[0]][l1_keys[1]] = value
                return data
        except FileNotFoundError:
            raise

    def save(self, data: dict):
        """Save configuration data to this source.

        This method saves the configuration data to the dotenv file specified
        during the initialization of this class.

        Args:
            data (dict): The configuration data to save.

        Raises:
            PermissionError: If the source is read-only.
        """
        if self.readonly:
            raise PermissionError("This source is read-only.")

        raise NotImplementedError("This source does not support saving.")
