from abc import abstractmethod
from typing import Any
from athenaeum.crawl.spiders.base_spider import BaseSpider
from athenaeum.crawl.spiders.mixins.cp_mixin import CpMixin


class BaseCpSpider(BaseSpider, CpMixin):
    @abstractmethod
    def start_requests(self, *args: Any, **kwargs: Any) -> Any:
        pass
