from peewee import MySQLDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_db_orm(*, settings_object: Optional[LazySettings] = None, **db_config_item: Dict[str, Any]) -> Any:
    db_orm = None

    db_config = {
        'host': None,
        'port': None,
        'user': None,
        'password': None,
        'database': None,
        'charset': 'utf8mb4',
        'use_unicode': True,
        'init_command': "SET time_zone='+8:00'"
    }

    if settings_object is None and not db_config_item:
        return db_orm

    if settings_object is not None:
        db_config['host'] = settings_object.MYSQL_HOST
        db_config['port'] = settings_object.MYSQL_PORT
        db_config['user'] = settings_object.MYSQL_USERNAME
        db_config['password'] = settings_object.MYSQL_PASSWORD
        db_config['database'] = settings_object.MYSQL_DBNAME

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    db_orm = MySQLDatabase(**db_config)

    return db_orm
