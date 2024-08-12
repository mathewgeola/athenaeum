from mongoengine import connect
from config import settings  # type: ignore

db_config = {
    "db": settings.MONGO_DBNAME,
    "host": settings.MONGO_HOST,
    "port": settings.MONGO_PORT,
    "username": settings.MONGO_USERNAME,
    "password": settings.MONGO_PASSWORD,
}
mongo_db_orm = connect(**db_config)
