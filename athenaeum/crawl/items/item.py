from copy import deepcopy
from pprint import pformat
from collections.abc import MutableMapping
from typing import Optional, Dict, Any, Iterator, Type
from typing_extensions import Self
from ..models.model import Model
from ..errors import ItemInitError, ItemGetAttributeError
from ...metas import BasesAttrsMergeMeta


class Field(object):
    pass


class ItemMeta(BasesAttrsMergeMeta):
    def __new__(mcs, name, bases, attrs):
        created_class = super().__new__(mcs, name, bases, attrs)
        attrs = created_class.__dict__
        created_class._fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        return created_class


class Item(MutableMapping, metaclass=ItemMeta):
    _fields: Dict

    def __init__(self, *args, **kwargs):
        self._data = dict()

        self.is_store: Optional[bool] = None
        self.Model: Optional[Type[Model]] = None

        if args:
            raise ItemInitError(f'Position args is not supported, please use keyword args!')
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} _data: {pformat(dict(self))}>'

    __str__ = __repr__

    def __setitem__(self, key, value) -> None:  # MutableMapping
        if key in self._fields:
            self._data[key] = value
        else:
            raise KeyError(f'Does not support field: {key}!')

    def __delitem__(self, key) -> None:  # MutableMapping
        del self._data[key]

    def __getitem__(self, key) -> Any:  # Mapping
        return self._data[key]

    def __len__(self) -> int:  # Collection
        return len(self._data)

    def __iter__(self) -> Iterator:  # Iterable
        return iter(self._data)

    def __setattr__(self, key, value) -> None:
        if key not in ['_data', 'is_store', 'Model']:
            raise AttributeError(f'Please use `item[{key!r}] = {value!r}` to set field value!')
        super().__setattr__(key, value)

    def __getattr__(self, key) -> None:
        raise AttributeError(f'Does not support field: {key}, please use the `{key}` field to the {self}, '
                             f'and use item[{key!r}] to get field value!')

    def __getattribute__(self, key) -> Any:
        print(key)
        _fields = super().__getattribute__('_fields')
        if key in _fields:
            raise ItemGetAttributeError(f'Please use item[{key!r}] to get field value!')
        return super().__getattribute__(key)

    def to_dict(self) -> Dict:
        return self._data

    def copy(self) -> Self:
        return deepcopy(self)
