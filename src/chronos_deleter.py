#!/usr/bin/python3
from logger import log
from database import Database



# checks for unsent timeentries
#

# config

db = Database()

log.warning("deleting old entries")

db.delete_time_entries_where_old()
db.close_connection()
