import inspect
from abc import abstractmethod
from typing import Optional, Any, Type
from athenaeum.crawl.items.base_item import BaseItem
from athenaeum.metas import BasesAttrsMergeMeta
from athenaeum.crawl.spiders.base_data_spider import BaseDataSpider
from athenaeum.project import camel_to_snake


class BaseSpiderMeta(BasesAttrsMergeMeta):

    def __new__(mcs, name, bases, attrs):
        if attrs.get('name') is None:
            attrs['name'] = camel_to_snake(name)
        cls = super().__new__(mcs, name, bases, attrs)
        attrs = cls.__dict__
        if not inspect.isabstract(cls):
            if attrs.get('source') is None:
                raise ValueError(f'`{name}.source` 必须提供！')
            if attrs.get('url') is None:
                raise ValueError(f'`{name}.url` 必须提供！')
        return cls


class BaseSpider(BaseDataSpider, metaclass=BaseSpiderMeta):
    name: str
    source: Optional[str] = None
    url: Optional[str] = None
    start_datetime: str = '2024-08-08 00:00:00'
    limit_interval: int = 86400
    run_interval: int = 86400
    status: int = 1

    Item: Type[BaseItem] = BaseItem

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} name：{self.name}>'

    __str__ = __repr__

    @abstractmethod
    def start_requests(self, *args: Any, **kwargs: Any) -> Any:
        pass
