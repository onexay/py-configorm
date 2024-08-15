"""
ENVSource: A class for a environment variable configuration source.

This module contains the ENVSource class, a class for a environment variable
configuration source. It provides methods to load and save configuration data
from/to environment variables.

Attributes:
    ENVSource (ENVSource): The ENVSource class.

"""

import os

from configorm.sources.base import SourceBase


class ENVSource(SourceBase):
    """
    Class for a environment variable configuration source.

    This class is a subclass of `SourceBase` and represents a environment variable
    configuration source. It provides methods to load and save configuration data
    from/to environment variables.

    Attributes:
        prefix (str): The prefix for environment variables.
        nesting_slug (str): The string used to replace dots in the configuration
            keys for environment variable names.

    Methods:
        __init__(self, prefix: str = "CFGORM", readonly: bool = True, nesting_slug: str = "__"):
            Initializes a new instance of `ENVSource`.

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
        self, prefix: str = "CFGORM", readonly: bool = True, nesting_slug: str = "__"
    ):
        super().__init__(readonly)
        self._prefix = prefix
        self._nesting_slug = nesting_slug

    def load(self) -> dict:
        """Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        return {
            k[len(self._prefix) :]: v
            for k, v in os.environ.items()
            if k.startswith(self._prefix)
        }

    def save(self, data: dict):
        """Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        if self.readonly:
            raise PermissionError("This source is read-only.")

        for k, v in data.items():
            os.environ[self._prefix + k.replace(self._nesting_slug, ".")] = str(v)
