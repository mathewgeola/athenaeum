from mongoengine import connect
from config import settings  # type: ignore

db_config = {
    'db': settings.MONGODB_DBNAME,
    'host': settings.MONGODB_HOST,
    'port': settings.MONGODB_PORT,
    'username': settings.MONGODB_USERNAME,
    'password': settings.MONGODB_PASSWORD,
}
mongodb_orm = connect(**db_config)
