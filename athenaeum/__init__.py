import sys
from athenaeum.logger import logger

try:
    from config import settings  # type: ignore
except ModuleNotFoundError:
    logger.error(f'请使用 athenaeum 来创建配置文件')
    sys.exit()
