import peewee
from config import settings  # type: ignore

sqlite_orm = peewee.SqliteDatabase(settings.SQLITE_PATH)
