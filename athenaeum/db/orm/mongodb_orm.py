from mongoengine import connect
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_db_orm(*, settings_object: Optional[LazySettings] = None, **db_config_item: Dict[str, Any]) -> Any:
    db_orm = None

    db_config = {
        'host': None,
        'port': None,
        'username': None,
        'password': None,
        'db': None,
    }

    if settings_object is None and not db_config_item:
        return db_orm

    if settings_object is not None:
        db_config['host'] = settings_object.MONGODB_HOST
        db_config['port'] = settings_object.MONGODB_PORT
        db_config['username'] = settings_object.MONGODB_USERNAME
        db_config['password'] = settings_object.MONGODB_PASSWORD
        db_config['db'] = settings_object.MONGODB_DBNAME

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    db_orm = connect(**db_config)

    return db_orm
