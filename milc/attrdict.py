from collections import UserDict
from typing import Any


class AttrDict(UserDict):
    """A dictionary that can also be accessed by attribute.
    """
    def __getattr__(self, key: Any) -> Any:
        return self.__getitem__(key)


class SparseAttrDict(AttrDict):
    """A dictionary that can also be accessed by attribute.

    This class never raises IndexError, instead it will return None if a
    key does not yet exist.
    """
    def __getitem__(self, key: Any) -> Any:
        """Returns an item, creating it if it doesn't already exist
        """
        if key not in self.data:
            self.data[key] = None

        return self.data[key]
