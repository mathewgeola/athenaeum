from athenaeum.crawl.models.peewee_model import PeeweeModel
from athenaeum.db.orm.mysql_orm import mysql_orm
from athenaeum.project import camel_to_snake


class MysqlModel(PeeweeModel):
    """
    https://docs.peewee-orm.com/en/3.15.3/peewee/api.html#ColumnBase

    """

    class Meta:
        database = mysql_orm
        table_function = lambda model_class: camel_to_snake(model_class.__name__)  # noqa
