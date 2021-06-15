#!/usr/bin/python3

import os
from chronos.database import Database
import logging
import logging.config

logging.config.fileConfig(os.environ.get("LOGGING_CONFIG_PATH"))
log = logging.getLogger("chronosLogger")

# checks for unsent timeentries
#

# config

db = Database()

log.warning("deleting old entries")

db.delete_time_entries_where_old()
