from abc import abstractmethod
from pprint import pformat
from typing import Any, Optional
from athenaeum.crawl.items.item import Item
from athenaeum.crawl.spiders.spider import Spider


class BaseDataSpider(Spider):

    @abstractmethod
    def start_requests(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def save_item(self, item: Optional[Item] = None) -> None:
        if item is None:
            self.logger.debug(f'取消入库操作，item：`{item}`')
            return

        if item.is_store is False:
            self.logger.debug(f'取消入库操作，item：`{item}`')
            return

        data = item.to_dict()

        model_cls = item.Model
        if model_cls is None:
            raise ValueError(f'model_cls：`{model_cls}` 不能为 None！')
        model_ins = model_cls()
        model_ins.store(data)

        if data['status'] == 1:
            self.logger.success(f'正常数据保存成功，data：`{pformat(data)}`')
        else:
            self.logger.error(f'异常数据保存成功，data：`{pformat(data)}`!')
