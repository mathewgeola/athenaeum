from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from athenaeum.crawl.models.peewee_model import PeeweeModel


class ModelMeta(type):
    def __subclasscheck__(cls, subclass):
        if issubclass(subclass, PeeweeModel):  # 只要是指定 Model 的子类，就认定为是本 Model 的子类
            return True
        return False


class Model(ABC, metaclass=ModelMeta):

    @abstractmethod
    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        pass
