from peewee import Model, CharField, SmallIntegerField, DateTimeField, SQL, Field
from playhouse.mysql_ext import JSONField as mysql_ext_JSONField
from playhouse.sqlite_ext import JSONField as sqlite_ext_JSONField
from typing import Optional, Union, Dict, Any, Type
from athenaeum.crawl.models.model import ModelMeta
from athenaeum.crawl.models.peewee_model import PeeweeModel
from athenaeum.project import gen_data_id


def get_json_field(db_type: str) -> Union[Type[mysql_ext_JSONField], Type[sqlite_ext_JSONField]]:
    if db_type == 'mysql':
        return mysql_ext_JSONField
    elif db_type == 'sqlite':
        return sqlite_ext_JSONField
    else:
        raise ValueError(f'不支持 db_type：`{db_type}`！')


class BaseDataPeeweeModelMeta(ModelMeta):
    def __new__(cls, name, bases, attrs):
        if attrs.get('data_columns') is None:
            if (db_type := attrs.get('_db_type')) is None:
                raise ValueError(f'name：`{name}` 类属性 _db_type 值不能为 `{db_type}`!')
            else:
                attrs['data_columns'] = get_json_field(db_type)(default=None, verbose_name='数据字段')
        return super().__new__(cls, name, bases, attrs)


class BaseDataPeeweeModel(PeeweeModel, metaclass=BaseDataPeeweeModelMeta):
    _db_type: Optional[str] = None
    data_id = CharField(unique=True, max_length=32, verbose_name='数据ID')
    data_columns: Optional[Field] = None
    status = SmallIntegerField(index=True, default=1, constraints=[SQL('DEFAULT 1')], verbose_name='状态')
    create_time = DateTimeField(index=True, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], verbose_name='创建时间')
    update_time = DateTimeField(index=True, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')],
                                verbose_name='更新时间')

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id：`{self.id}` data_id：`{self.data_id}`>'

    __str__ = __repr__

    def get_data_id(self) -> str:
        data_columns = self.data.get('data_columns')
        assert (data_columns is not None and isinstance(data_columns, list) and
                all(map(lambda x: isinstance(x, str), data_columns))), '`data_columns` 值必须是字符串列表！'
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
        if data is not None:
            self.data = data
        data_id = self.get_data_id()
        row = self.get_row_by_data_id(data_id)
        if row is None:
            sql = self.insert(**self.data)
            is_insert = True
        else:
            sql = self.update(**self.data).where(self.__class__.data_id == data_id)
            is_insert = False
        with self.Meta.database.atomic():
            ret = sql.execute()
            if is_insert:
                self.__data__['id'] = ret
            else:
                if row.__data__.get('id'):
                    self.__data__['id'] = row.__data__.get('id')
        return is_insert
