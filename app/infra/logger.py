import logging
from app.config.config_resolver import ConfigResolver
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_level_number(level_name: str) -> int:
    name_to_level = {
        'CRITICAL': 50,
        'FATAL': 50,
        'ERROR': 40,
        'WARN': 30,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10,
        'NOTSET': 0,
    }

    level = name_to_level.get(level_name)

    return level if level else name_to_level['NOTSET']


def get_logger(module_name: str):
    config_resolver = ConfigResolver()

    logger = logging.getLogger(module_name)
    logger.setLevel(_get_level_number(config_resolver.log_level.upper()))

    c_handler = logging.StreamHandler()

    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)

    logger.addHandler(c_handler)

    return logger



