"""
TOMLSource: Class which implements a TOML configuration source.

This module provides methods and attributes to load and save configuration
from TOML files.

Attributes:
    TOMLSource (TOMLSource): The TOMLSource class.
"""

from pathlib import Path
from typing import Any, Dict

import toml
from py_configorm.sources.base import BaseSource


class TOMLSource(BaseSource):
    """
    TOML configuration source.

    This class is a subclass of `BaseSource` and represents a TOML configuration
    source. It uses `toml` package to load and save configuration data from/to
    a TOML file.

    ```toml
    Key1 = "Value1"
    [Key2]
    Key21 = "Value21"
    Key22 = "Value22"
    ```

    ```python
    data = {
        "Key1": "Value1",
        "Key2": {
            "Key21": "Value21",
            "Key22": "Value22",
        },
    }
    ```

    Attributes:
        filepath (Path): The path to the TOML configuration file in URL syntax.
        readonly (bool): Whether the source is read-only, default is `True`.

    Methods:
        load(self) -> dict:
            Load configuration data from this source.

            Returns:
                dict: The loaded configuration data.

        save(self, data: dict):
            Save configuration data to this source.

            Args:
                data (dict): The configuration data to save.
    """

    def __init__(self, filepath: Path, readonly: bool = True):
        super().__init__(filepath, readonly)

    def load(self) -> Dict[str, Any]:
        """
        Load configuration data from this source.

        This method loads the configuration data from the TOML file specified
        during the initialization of this class. Note that attributes in TOML
        file MUST match with attributes defined in [py_configorm.core.ConfigSchema][].

        Returns:
            dict: The loaded configuration data.
        """
        try:
            with open(self.filepath.resolve(), "r") as f:
                # Load raw data from TOML file, at this point it's just a
                # dictionary containing the TOML data.
                #
                return toml.load(f)
        except Exception as e:
            raise e

    def save(self, data: dict):
        """
        Save configuration data to this source.

        This method saves the configuration data to the TOML file specified
        during the initialization of this class. Note that attributes in TOML
        file MUST match with attributes defined in [py_configorm.core.ConfigSchema][].

        Args:
            data (dict): _description_

        Raises:
            PermissionError: _description_
        """
        try:
            if self.readonly:
                raise PermissionError("This source is read-only.")

            with open(self.filepath, "w") as f:
                toml.dump(data, f)
        except Exception as e:
            raise e
