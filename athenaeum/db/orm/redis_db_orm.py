from walrus import Database
from config import settings  # type: ignore

db_config = {
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
    'db': settings.REDIS_DBNAME,
    'password': settings.REDIS_PASSWORD,
}
redis_db_orm = Database(**db_config)
