from athenaeum.crawl.models.base_peewee_data_model import BasePeeweeDataModel


class BaseDataSqliteModel(BasePeeweeDataModel):
    _db_type = 'sqlite'
