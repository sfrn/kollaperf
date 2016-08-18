#!/usr/bin/env python3
import sys, os
import logging
import threading
import time
from logging.handlers import RotatingFileHandler

from kollaperf.config import settings
from kollaperf.machine import Machine

log = logging.getLogger(__name__)

WAIT_UNTIL_RESTART= settings['restart_seconds']

class WaitThread(threading.Thread):
    def run(self):
        time.sleep(WAIT_UNTIL_RESTART)
        log.info('Kill me automatically ...')
        os._exit(0)

formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("kolla.log", maxBytes=settings['log']['max_bytes'], backupCount=settings['log']['backup_count'])
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root_logger.addHandler(consoleHandler)

if len(sys.argv) > 1 and sys.argv[1] == '-r':
    log.info('Kill after {} seconds ...'.format(WAIT_UNTIL_RESTART))
    WaitThread().start()

machine = Machine()
machine.run_forever()
