"""
ConfigORM - A simple configuration library.

This is a python library for handling configuration data.

"""

from abc import ABC, abstractmethod


class SourceBase(ABC):
    """
    Base class for all configuration sources.

    This class is an abstract base class for all configuration sources.
    It defines the basic interface for loading and saving configuration
    data.

    Attributes:
        readonly (bool): Whether the source is read-only.
    """

    def __init__(self, readonly: bool = True):
        self._readonly = readonly

    @abstractmethod
    def load(self) -> dict:
        """
        Load configuration data from this source.

        Returns:
            dict: The loaded configuration data.
        """
        pass

    @abstractmethod
    def save(self, data: dict):
        """
        Save configuration data to this source.

        Args:
            data (dict): The configuration data to save.
        """
        pass

    # @abstractmethod
    # def reload(self):
    #     """
    #     Reload configuration data from this source.

    #     This method is called when the application is reloaded and the
    #     configuration data must be reloaded from the source.

    #     """
    #     pass

    @property
    def readonly(self) -> bool:
        return self._readonly
