import logging

from kollaperf.machine import Machine

formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("kolla.log")
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root_logger.addHandler(consoleHandler)

machine = Machine()
machine.run_forever()
