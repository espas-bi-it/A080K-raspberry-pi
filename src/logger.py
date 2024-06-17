import os
import logging
import logging.config

logging.config.fileConfig(os.environ.get("LOGGING_CONFIG_PATH"))
log = logging.getLogger("chronosLogger")