from athenaeum.crawl.models.peewee_model import PeeweeModel
from athenaeum.db.orm.sqlite_orm import sqlite_orm
from athenaeum.project import camel_to_snake


class __SqliteModel(PeeweeModel):
    class Meta:
        database = sqlite_orm
        table_function = lambda model_class: camel_to_snake(model_class.__name__)  # noqa
