from typing import Optional, Dict, Any
from peewee import CharField, SmallIntegerField, DateTimeField, SQL, Model
from playhouse.mysql_ext import JSONField
from athenaeum.crawl.models.mysql.mysql_model import MysqlModel
from athenaeum.db.orm.mysql_db_orm import mysql_db_orm

from athenaeum.project import gen_data_id


class BaseDataMysqlModel(MysqlModel):
    data_id = CharField(unique=True, max_length=32, verbose_name='数据ID')
    data_columns = JSONField(default=None, verbose_name='数据字段')
    status = SmallIntegerField(index=True, default=1, constraints=[SQL('DEFAULT 1')], verbose_name='状态')
    create_time = DateTimeField(index=True, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], verbose_name='创建时间')
    update_time = DateTimeField(index=True, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')],
                                verbose_name='更新时间')

    def get_data_id(self) -> str:
        data_columns = self.data.get('ux_columns')
        assert (data_columns is not None and isinstance(data_columns, list) and
                all(map(lambda x: isinstance(x, str), data_columns))), '`ux_columns` 值必须是字符串列表！'
        for data_column in data_columns:
            if data_column not in self.data:
                raise ValueError(f'data_columns 中的 `{data_column}` 字段没有赋值，计算得到的 data_id 无效！')
        data_id = self.data.get('data_id')
        if data_id is None:
            data_id = gen_data_id(keys=data_columns, item=self.data)
            self.__data__['data_id'] = data_id
        return data_id

    def get_row_by_data_id(self, data_id: Optional[str] = None) -> Optional[Model]:
        if data_id is None:
            data_id = self.get_data_id()
        return self.get_or_none(self.__class__.data_id == data_id)

    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        self.data = data
        data_id = self.get_data_id()
        row = self.get_row_by_data_id(data_id)
        if row is None:
            sql = self.insert(**self.data)
            is_insert = True
        else:
            sql = self.update(**self.data).where(self.__class__.data_id == data_id)
            is_insert = False
        with mysql_db_orm.atomic():
            ret = sql.execute()
            if is_insert:
                self.__data__['id'] = ret
            else:
                if row.__data__.get('id'):
                    self.__data__['id'] = row.__data__.get('id')
        return is_insert
