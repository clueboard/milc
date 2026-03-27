from collections.abc import MutableMapping
from typing import Any, Iterator


class AttrDict(MutableMapping):
    """A dictionary that can also be accessed by attribute.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._data: dict = {}

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: Any) -> None:
        del self._data[key]

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __getattr__(self, key: Any) -> Any:
        if key.startswith('_'):
            raise AttributeError(key)
        return self.__getitem__(key)


class SparseAttrDict(AttrDict):
    """A dictionary that can also be accessed by attribute.

    This class never raises IndexError, instead it will return None if a
    key does not yet exist.
    """
    def __getitem__(self, key: Any) -> Any:
        """Returns an item, creating it if it doesn't already exist
        """
        if key not in self._data:
            self._data[key] = None

        return self._data[key]
