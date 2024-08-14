from athenaeum.render import Render
from athenaeum.logger import logger

try:
    from config import settings  # type: ignore
except ModuleNotFoundError:
    Render.render_project()
