import os
import logging as log

from dotenv import load_dotenv
import mysql.connector
from datetime import datetime, timedelta

load_dotenv()


class Database:
    def __init__(self):
        try:
            self.init_db()
            

        except mysql.connector.Error as e:
            log.error(e)
            print(e)
        return

    def init_db(self):
        # build up connection
        self.connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', default="localhost"),
            user=os.environ.get('DB_USER', default="root"),
            password=os.environ.get('DB_PASSWORD', default=""),
            database=os.environ.get('DB_DATABASE', default="badging"),
            autocommit=True)

    def get_cursor(self):
        try:
            # is connection valid?
            self.connection.ping(reconnect=True, attempts=3, delay=5)
        except mysql.connector.Error as err:
            # connection might has had a timeout
            # reconnect db
            self.init_db()
        # get cursor
        return self.connection.cursor()

    def add_time_entry(self, rfid, time):
        # adds new timeentry to db
        dbCursor = self.get_cursor()
        dbCursor.execute(
            "INSERT INTO time_entries (rfid, scanned_at, sent_at) VALUES ('%s', '%s', null)" % (rfid, time))

    def get_time_entries_where_unsent(self):
        # returns all timeentries which have not been sent to server
        dbCursor = self.get_cursor()
        dbCursor.execute(
            "SELECT * FROM time_entries WHERE sent_at IS NULL AND does_not_exist = 0")
        return dbCursor.fetchall()

    def set_time_entry_sent(self, id): 
        log.info("setting timeentry as sent")
        dbCursor = self.get_cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dbCursor.execute("UPDATE time_entries SET sent_at=%s WHERE id = %s", params=(timestamp, id))

    def set_time_entry_not_exist(self, id):
        log.info("setting timeentry to does not exist")
        dbCursor = self.get_cursor()

        dbCursor.execute("UPDATE time_entries SET does_not_exist=1 WHERE id = %s" % id)

    def delete_time_entries_where_old(self):
        log.info("deleting timeentries where old")
        dbCursor = self.get_cursor()
        # delete timeentries which are older than X days
        date = datetime.now() - \
            timedelta(days=int(os.environ['TIMEENTRIES_DELETE_AFTER_DAYS']))
        dbCursor.execute('DELETE FROM time_entries WHERE scanned_at < "%s" AND sent_at IS NOT NULL',
                              params=date.strftime("%Y-%m-%d %H:%M:%S"))

    def close_connection(self):
        # close connection to db
        self.connection.close()
