# Generate semi-random time entries to test backend connection and handling of simultaneous entry sending and switched times

import argparse
import mysql.connector
from datetime import datetime, timedelta
import random

parser = argparse.ArgumentParser(description="Create new time entries for the local database")
# Add commandline arguments to easily switch the mysql connection
parser.add_argument("database", help="The name of the database")
parser.add_argument("table", help="The table to use inside the database")
parser.add_argument("rfid", help="The rfid of the card to use")
parser.add_argument("--host", help="The host of the database server", default="localhost")
parser.add_argument("--user", "-u", help="The user used for the database actions", default="root")
parser.add_argument("--password", "-p", help="The password of --user", default="root")
parser.add_argument("--count", "-c", help="The number of entries to insert into the database", type=int, default=7)
args = parser.parse_args()

# Connect to mysql server using the given arguments
connection = mysql.connector.connect(
	host=args.host,
	user=args.user,
	password=args.password,
	database=args.database,
	autocommit=True
)

try:
	connection.ping(reconnect=True, attempts=3, delay=5)
except mysql.connector.Error as err:
	print("Error while trying to connect to database: %s" % (err, ))
	print("Exiting the program")
	exit(1)

db_cursor = connection.cursor()

# Create semi-random datetimes using the current datetime, args.count and random
for i in range(args.count):
	subtract_day = random.randrange(0, args.count)
	subtract_hour = random.randrange(0, 23)
	subtract_minute = random.randrange(0, 59)
	subtract_second = random.randrange(0, 59)
	time = datetime.now() - timedelta(days=subtract_day, hours=subtract_hour, minutes=subtract_minute, seconds=subtract_second)

	db_cursor.execute("INSERT INTO %s (rfid, scanned_at, sent_at) VALUES ('%s', '%s', null)" % (args.table, args.rfid, time.strftime("%Y-%m-%d %H:%M:%S")))
