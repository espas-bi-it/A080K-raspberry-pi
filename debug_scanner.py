#!/usr/bin/python3

import os
import time
import logging as log
import logging.config
from dotenv import load_dotenv

from chronos.mifare_scanner import MifareScanner

import pygame as pg

file_path = os.path.dirname(__file__)

load_dotenv()

logging.config.fileConfig(os.environ.get("LOGGING_CONFIG_PATH"))
log = logging.getLogger("chronosLogger")

log.debug("boot")


log.debug("load env")

scanner = MifareScanner()
log.debug("initialized MifareScanner")

scanner.process_rfid(rfid="python debug")
