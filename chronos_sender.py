#!/usr/bin/python3

import os
from chronos.sender import Sender
import logging
import logging.config

file_path = os.path.dirname(__file__)


logging.config.fileConfig(os.environ.get("LOGGING_CONFIG_PATH"))
log = logging.getLogger("chronosLogger")

# checks for unsent timeentries
#

# config

sender = Sender()

log.debug("sender boot")

sender.send_unsent()
