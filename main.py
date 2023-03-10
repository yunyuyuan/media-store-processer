import time
from os import path
import logging
from logging.handlers import RotatingFileHandler

from src import exiftool, get_args

logFile = path.join(path.dirname(__file__), 'exiftool.log')
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1024*1024,
                                 backupCount=0, encoding=None, delay=False)
my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'))
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

if __name__ == '__main__':
    args = get_args()
    exiftool(app_log)
