#!/usr/bin/python3

import os
from sender import Sender
from logger import log


file_path = os.path.dirname(__file__)


sender = Sender()

log.debug("sender boot")

sender.send_unsent()
