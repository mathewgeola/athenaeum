from peewee import Model, PrimaryKeyField, Field
from typing import Optional, Union, List, Dict, Any
from athenaeum.logger import logger


class PeeweeModel(Model):
    logger = logger

    id = PrimaryKeyField(verbose_name='ID')

    def __init__(self, create_table: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if create_table:
            if not self.table_exists():
                self.create_table()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id：`{self.id}`>'

    __str__ = __repr__

    @property
    def table_name(self) -> str:
        return self._meta.table_name

    @property
    def fields(self) -> Dict[str, Field]:  # 模型字段相关
        return self._meta.fields

    @property
    def columns(self) -> Dict[str, Field]:  # 表列相关
        return self._meta.columns

    @property
    def field_names(self) -> List[str]:
        return [field_name for field_name in self.fields.keys()]

    @property
    def column_names(self) -> List[str]:
        return [column_names for column_names in self.columns.keys()]

    @property
    def field_column_names(self) -> List[str]:
        return list(set(self.field_names + self.column_names))

    @property
    def fields_to_verbose_name(self) -> Dict[str, str]:
        return {k: v.verbose_name for k, v in self.fields.items()}

    @property
    def columns_to_verbose_name(self) -> Dict[str, str]:
        return {k: v.verbose_name for k, v in self.columns.items()}

    @property
    def data(self) -> Dict[str, Any]:
        return self.__data__

    @data.setter
    def data(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if key in self.field_column_names:
                self.__data__[key] = value
            else:
                self.logger.warning(f'字段 `{key}` 没有定义在 `{self.__class__.__name__}` 类中，不能设置值！')

    def get_id(self) -> Union[None, int, str]:
        id_ = self.data.get('id')
        return id_

    def get_row_by_data_id(self, id_: Union[None, int, str] = None) -> Optional[Model]:
        if id_ is None:
            id_ = self.get_id()
        if id_ is None:
            return
        return self.get_or_none(self.__class__.id == id_)

    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        if data is not None:
            self.data = data
        id_ = self.get_id()
        row = self.get_row_by_id(id_)
        if row is None:
            sql = self.insert(**self.data)
            is_insert = True
        else:
            sql = self.update(**self.data).where(self.__class__.id == id_)
            is_insert = False
        with self.Meta.database.atomic():
            ret = sql.execute()
            if is_insert:
                self.__data__['id'] = ret
            else:
                if row.__data__.get('id'):
                    self.__data__['id'] = row.__data__.get('id')
        return is_insert
