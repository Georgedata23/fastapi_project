import json

import logging.config
from logging import getLogger

with open("app/logging_dir/logging.conf") as file:
    config = json.load(file)

logging.config.dictConfig(config)
logger = getLogger()
logger.info("logging is working!")