from peewee import MySQLDatabase
from config import settings  # type: ignore

db_config = {
    "host": settings.MYSQL_HOST,
    "port": settings.MYSQL_PORT,
    "user": settings.MYSQL_USERNAME,
    "password": settings.MYSQL_PASSWORD,
    "database": settings.MYSQL_DBNAME,
    "charset": "utf8mb4",
    "use_unicode": True,
    "init_command": "SET time_zone='+8:00'"
}
mysql_db_orm = MySQLDatabase(**db_config)
