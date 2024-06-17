import os

from datetime import datetime
from datetime import timedelta
import logging as log
from database import Database
from sound_player import playSound

import nxppy as nxppy


class MifareScanner:
    def __init__(self):
        self.db = Database()
        self.lastRfid = None
        self.lastRfidTime = datetime.now()
        self.mifare = nxppy.Mifare()

    def scan_rfid(self):
        # retrieve rfid from chips
        try:
            rfid = self.mifare.select()
            return rfid
        except nxppy.SelectError:
            # SelectError is raised if no card is in the field. as e:
            return None

    def process_rfid(self, rfid):
        log.debug('processing rfid scan')

        if rfid != self.lastRfid or self.lastRfidTime < (datetime.now() - timedelta(seconds=30)):
            log.info("inserting new timeentry - " + rfid)

            time = datetime.now()  # get time of scan
            self.db.add_time_entry(  # add new entry in database
                rfid=rfid,
                time=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            playSound(os.environ.get("SOUND_PATH"))
            
                
            self.lastRfid = rfid  # save rfid + scan time
            self.lastRfidTime = time

            self.db.close_connection()

            return

        # when duplicate and previous entry less than 5 mins ago
        else:
            log.debug('duplicate scan - playing sound only')

            playSound(os.environ.get("SOUND_ERROR_PATH"))
