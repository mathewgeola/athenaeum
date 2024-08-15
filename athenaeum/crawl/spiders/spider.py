from abc import ABC, abstractmethod
from typing import Optional, Any
from typing_extensions import Self  # type: ignore
from athenaeum.logger import logger
from athenaeum.crawl.items.item import Item


class Spider(ABC):
    logger = logger

    def __init__(self, *args: Any, **kwargs: Any):
        self.init_args = args
        self.init_kwargs = kwargs

    @classmethod
    def create_instance(cls, *args: Any, **kwargs: Any) -> Self:
        return cls(*args, **kwargs)

    @abstractmethod
    def start_requests(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def parse(self, *args, **kwargs):
        pass

    def parse_first(self, *args, **kwargs):
        pass

    def parse_second(self, *args, **kwargs):
        pass

    def parse_third(self, *args, **kwargs):
        pass

    def parse_fourth(self, *args, **kwargs):
        pass

    def parse_fifth(self, *args, **kwargs):
        pass

    def parse_sixth(self, *args, **kwargs):
        pass

    def parse_seventh(self, *args, **kwargs):
        pass

    def parse_eighth(self, *args, **kwargs):
        pass

    def parse_ninth(self, *args, **kwargs):
        pass

    def parse_tenth(self, *args, **kwargs):
        pass

    def parse_eleventh(self, *args, **kwargs):
        pass

    def parse_twelfth(self, *args, **kwargs):
        pass

    def parse_thirteenth(self, *args, **kwargs):
        pass

    def parse_fourteenth(self, *args, **kwargs):
        pass

    def parse_fifteenth(self, *args, **kwargs):
        pass

    def parse_sixteenth(self, *args, **kwargs):
        pass

    def parse_seventeenth(self, *args, **kwargs):
        pass

    def parse_eighteenth(self, *args, **kwargs):
        pass

    def parse_nineteenth(self, *args, **kwargs):
        pass

    def parse_twentieth(self, *args, **kwargs):
        pass

    @abstractmethod
    def save_item(self, item: Optional[Item] = None) -> None:
        pass
