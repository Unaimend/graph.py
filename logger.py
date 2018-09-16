# pylint: skip-file
import logging
import sys
logger = logging.getLogger('debug_log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log', mode="w")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.ERROR)
logger.addHandler(fh)
logger.addHandler(ch)

ERROR = logging.ERROR
DEBUG = logging.DEBUG

