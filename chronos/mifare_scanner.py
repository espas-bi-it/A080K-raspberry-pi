import os

from datetime import datetime
from datetime import timedelta
import logging as log
from chronos.database import Database
from chronos.sound_player import SoundPlayer

import nxppy


class MifareScanner:
    def __init__(self):
        self.db = Database()
        self.lastRfid = None
        self.lastRfidTime = datetime.now()
        self.soundPlayer = SoundPlayer()
        self.mifare = nxppy.Mifare()
        

    def scan_rfid(self):
        # retrieve rfid from chips
        try:
            rfid = self.mifare.select()
            return rfid
        except nxppy.SelectError:
            # SelectError is raised if no card is in the field. as e:
            return None

    def scan_data(self):
        # scan for data on chip
        pass

    def process_rfid(self, rfid):
        log.debug('processing rfid scan')

        if (rfid != self.lastRfid) or self.lastRfidTime < (datetime.now() - timedelta(minutes=8)):
            log.info("inserting new timeentry - " + rfid)

            time = datetime.now()  # get time of scan
            self.db.add_time_entry(  # add new entry in database
                rfid=rfid,
                time=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            isrfidIn = self.db.get_time_entries_today_count(
                rfid=rfid)
            if isrfidIn % 2 == 1:  # play sound
                self.soundPlayer.play()
                # self.playSound(badge=badge, sound='./src/sounds/rfidn.mp3')
                pass
            else:
                self.soundPlayer.play()
                # self.playSound(badge=badge, sound='./src/sounds/rfidn.mp3')
                pass
            self.lastRfid = rfid  # save rfid + scan time
            self.lastRfidTime = time

            return

        # when duplicate and previous entry less than 5 mins ago
        else:
            # happend last scanHit of this rfid at least 2 minutes ago?
            if self.lastRfidTime < (datetime.now() - timedelta(seconds=15)):
                log.debug('duplicate scan - playing sound only')
                # decoy ping
                # self.playSound(badge=badge, sound='./src/sounds/rfidn.mp3')
                log.debug("duplicate scan - sound but no new timeentry")
                self.lastRfidTime = datetime.now()

                return

            log.debug('duplicate scan - doing nothing')
        return
        pass
