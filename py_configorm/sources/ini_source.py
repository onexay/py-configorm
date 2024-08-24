"""
INISource: Class which implements a INI configuration source.

This module provides methods and attributes to load and save configuration
from INI files.

Attributes:
    INISource (INISource): The INISource class.
"""
import configparser
from pathlib import Path
from py_configorm.sources.base import BaseSource


class INISource(BaseSource):
    """
    A source that reads configuration from an INI file.

    This class provides a way to read and parse configuration data from an INI
    file. The data can be accessed using standard dictionary-like syntax, making
    it easy to integrate with other parts of the application.

    Attributes:
        - file_path (str): The path to the INI file.
        - config_data (dict): A dictionary containing the parsed configuration
            data from the INI file.
    """

    def __ini__(self, file_path: Path | None, readonly: bool = True):
        super().__init__(file_path, readonly)

    def load(self) -> dict:
        try:
            with open(self.filepath, "r") as f:
                parser_ = configparser.ConfigParser()
                parser_.read_file(f)
                return {s: dict(parser_.items(s)) for s in parser_.sections()}
        except Exception as e:
            raise e

    def save(self, data: dict):
        try:
            if self.readonly:
                raise PermissionError("This source is readonly.")

            raise NotImplementedError("This source doesn't support save.")

        except Exception as e:
            raise e

    def reload(self) -> dict:
        pass
