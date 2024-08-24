"""
ENVSource: Class implementing a environment variable configuration source.

This module provides methods and attributes to load and save configuration
from environment variables.

Attributes:
    ENVSource (ENVSource): The ENVSource class.

"""

import os

from py_configorm.sources.base import BaseSource


class ENVSource(BaseSource):
    """
    Class for a environment variable configuration source.

    This class is a subclass of `SourceBase` and represents a environment variable
    configuration source. It provides methods to load and save configuration data
    from/to environment variables.

    Environment variables are defined as per `[PREFIX]_[KEY][NESTING_SLUG][SUBKEY] = [VALUE]`
    format. For example, if `PREFIX` is set to `CFGORM` and `NESTING_SLUG` is
    set to `__`, then environment variables will be defined as
    `CFGORM_[KEY]__[SUBKEY] = VALUE`. For providing bidirectional mutation operations
    for ORM, these variables need to be converted to a dictionary following the
    semantics of the user specified by subclassing [py_configorm.core.ConfigSchema][].

    This library only supports single level of nesting of configuration data, i.e.,
    for environment variables containing multiple `NESTING_SLUGS`, only the first
    `NESTING_SLUG` will be considered for nesting, the remaining will become the
    nested configuration attribute. For example, if environment variable is,
    `CFGORM_KEY1__NESTEDKEY2__NESTEDKEY3 = VALUE`, only `KEY1` will be considered
    for nesting and the remaining will become the nested configuration attribute as
    following,

    ```env    
    CFGORM_KEY1__NESTEDKEY1__NESTEDKEY1 = VALUE
    CFGORM_KEY2__NESTEDKEY1 = VALUE
    CFGORM_KEY3 = VALUE
    ```

    ```python
    data = {
        'KEY1': {
            'NESTEDKEY1__NESTEDKEY1': 'VALUE'
        },
        'KEY2': {
            'NESTEDKEY1': 'VALUE'
        },
        'KEY3': 'VALUE'
    }
    ```

    Attributes:
        prefix (str): The prefix for environment variables.
        nesting_slug (str): The string used to determine nesting in environment variables.

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
        self, prefix: str = "CFGORM_", readonly: bool = True, nesting_slug: str = "__"
    ):
        super().__init__(None, readonly)
        self._prefix = prefix
        self._nesting_slug = nesting_slug

    def load(self) -> dict:
        """Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        vars_ = {
            k[len(self._prefix) :]: v
            for k, v in os.environ.items()
            if k.startswith(self._prefix)
        }

        data = {}
        for key, value in vars_.items():
            l1_keys = key.split(self._nesting_slug, maxsplit=1)
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

    def save(self, data: dict):
        """Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        if self.readonly:
            raise PermissionError("This source is read-only.")

        for k0, v0 in data.items():
            if isinstance(v0, dict):
                for k1, v1 in v0.items():
                    if isinstance(v1, dict):
                        raise ValueError("Only one level of nesting is supported.")
                    os.environ[self._prefix + k0 + self._nesting_slug + k1] = v1
            else:
                os.environ[self._prefix + k0] = v0
