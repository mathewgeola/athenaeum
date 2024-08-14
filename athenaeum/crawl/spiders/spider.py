from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import Self  # type: ignore
from athenaeum.crawl.items.item import Item


class Spider(ABC):

    def __init__(self, *args: Any, **kwargs: Any):
        self.init_args = args
        self.init_kwargs = kwargs

    @classmethod
    def create_instance(cls, *args: Any, **kwargs: Any) -> Self:
        return cls(*args, **kwargs)

    @abstractmethod
    def start_requests(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def save_item(self, item: Item) -> None:
        pass
