from athenaeum.crawl.models.peewee_data_model import PeeweeDataModel


class BaseDataMysqlModel(PeeweeDataModel):
    _db_type = 'mysql'
