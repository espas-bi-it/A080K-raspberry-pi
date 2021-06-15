#!/usr/bin/python3

import os
import time
import logging as log
import logging.config
from dotenv import load_dotenv

from chronos.mifare_scanner import MifareScanner

load_dotenv()

logging.config.fileConfig(os.environ.get("LOGGING_CONFIG_PATH"))
log = logging.getLogger("chronosLogger")

log.debug("boot")


log.debug("load env")

scanner = MifareScanner()
log.debug("initialized MifareScanner")

while True:
    rfid = scanner.scan_rfid()

    if rfid:
        # found rfid
        scanner.process_rfid(rfid=rfid)
        time.sleep(1)
    else:
        # nothing scanned
        time.sleep(0.2)
