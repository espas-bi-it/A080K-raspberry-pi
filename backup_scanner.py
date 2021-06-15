#!/usr/bin/python3

import os
import time
import threading
from datetime import datetime
from datetime import timedelta
import logging as log
from dotenv import load_dotenv

from chronos.mifare_scanner import MifareScanner
from chronos.soundplayer import SoundPlayer
from chronos.database import Database

class Scanner:

    def __init__(self):
        # self.mifare = nxppy.Mifare()
        self.db = Database()
        self.soundPlayer = SoundPlayer()
        self.lastRfid = None,
        self.lastRfidTime = datetime.now()

    # scanns for aviable nfc chips
    def scan(self):
        return "rfid"
        try:
            # rfid = self.mifare.select()
            return rfid
        except Exception as e:
            return None

    # scanned a badge

    def scanHit(self, badge):
        log.debug('processing scan hit')

        # last scan at least 5 min old?
        if (badge['rfid'] != self.lastRfid) or self.lastRfidTime < (datetime.now() - timedelta(minutes=8)):

            log.info("inserting new timeentry: " + badge['rfid'])

            # get time of scan
            time = datetime.now()

            # add new entry in database
            self.db.add_time_entry(
                rfid=badge['rfid'],
                time=time.strftime("%Y-%m-%d %H:%M:%S")
            )

            isBadgedIn = self.db.get_time_entries_today_count(
                rfid=badge['rfid'])
            
            # play sound
            if isBadgedIn % 2 == 1:
                self.playSound(badge=badge, sound='./src/sounds/badgein.mp3')
            else:
                self.playSound(badge=badge, sound='./src/sounds/badgein.mp3')
            # save rfid + scan time
            self.lastRfid = badge['rfid']
            self.lastRfidTime = time

            return

        # when duplicate and previous entry less than 5 mins ago
        else:
            # happend last scanHit of this rfid at least 2 minutes ago?
            if self.lastRfidTime < (datetime.now() - timedelta(seconds=15)):
                log.info('duplicate scan, playing sound only')
                # decoy ping
                self.playSound(badge=badge, sound='./src/sounds/badgein.mp3')
                log.info("duplicate scan, sound but no new timeentry")
                self.lastRfidTime = datetime.now()

                return

            log.info('duplicate scan, doing nothing')
        return

    # play sound
    def playSound(self, badge, sound):
        if sound:
            # threading.Thread(target=playsound, args=(sound,), daemon=True).start()
            # playsound(sound)
            time.sleep(0.2)
        else:
            # TODO decide which sound to play
            # playsound(soundfile)
            pass
        log.info("playing sound")
