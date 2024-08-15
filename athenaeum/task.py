import time
import random
from multiprocessing import Process
from typing import Any
from athenaeum.logger import logger


class Task(Process):
    logger = logger

    def run(self, *args: Any, **kwargs: Any) -> None:
        while True:
            try:
                result = self.action()
            except Exception as exception:
                self.logger.exception(f'exception：{exception}！')
            else:
                return result
            finally:
                secs = random.uniform(1, 3)
                self.logger.debug(f'休眠{secs}秒')
                time.sleep(secs)

    def action(self) -> Any:
        pass
