"""
ConfigORM - A simple configuration library.

This is a python library for handling configuration data.

"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

class BaseSource(ABC):
    """
    Base class for all configuration sources.

    This class is an abstract base class for all configuration sources.
    It defines the basic interface for loading and saving configuration
    data.

    Attributes:
        filepath (Path): The path to the source configuration file.
        readonly (bool): Whether the source is read-only.
    """

    def __init__(self, filepath: Path | None, readonly: bool = True):
        self._readonly = readonly
        self._filepath = filepath

    @abstractmethod
    def load(self) -> Dict[Any, Any]:
        """
        Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        pass

    @abstractmethod
    def save(self, data: Dict[str, Any]):
        """
        Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        pass

    @property
    def filepath(self) -> Path | None:
        return self._filepath

    @property
    def readonly(self) -> bool:
        return self._readonly
