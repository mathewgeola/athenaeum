from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, Dict, Any

from peewee import Model as peeweeModel


class ModelMeta(ABCMeta):
    def __subclasscheck__(self, subclass):
        if issubclass(subclass, peeweeModel):
            return True
        return False


class Model(ABC, metaclass=ModelMeta):

    @abstractmethod
    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        pass
