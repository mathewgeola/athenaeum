from pathlib import Path
from dynaconf import Dynaconf
from athenaeum.logger import logger

ROOT_DIR = Path(__file__).absolute().parent

_SETTINGS_DIR = ROOT_DIR / 'settings'

_settings_files = [
    str(_SETTINGS_DIR / 'settings.toml'),
    str(_SETTINGS_DIR / 'settings.dev.toml'),
    str(_SETTINGS_DIR / 'settings.prod.toml'),
]
_dotenv_path = str(_SETTINGS_DIR / '.env')

settings = Dynaconf(
    settings_files=_settings_files,
    dotenv_path=_dotenv_path,
    envvar_prefix='DYNACONF',
    env_switcher='DYNACONF_ENV',
    environments=True,
    load_dotenv=True,
)

settings.ROOT_DIR = ROOT_DIR

logger.debug(f'current environment: {settings.current_env}.')

__all__ = [
    'settings',
]
