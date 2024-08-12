from sqlalchemy import create_engine
from config import settings  # type: ignore

mysql_uri = 'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DBNAME}?' \
            'charset=utf8mb4'.format(**settings)
mysql_engine = create_engine(mysql_uri)
