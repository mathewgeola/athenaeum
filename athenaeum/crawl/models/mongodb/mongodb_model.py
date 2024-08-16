from typing import Optional, Dict, Any

from athenaeum.crawl.models.model import Model


class MongodbModel(Model):
    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        pass
