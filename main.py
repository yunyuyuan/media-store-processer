import sys
import time
from os import popen
from os import path
import logging
from logging.handlers import RotatingFileHandler
from re import sub
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logFile = path.join(path.dirname(__file__), 'exiftool.log')
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1024*1024,
                                 backupCount=2, encoding=None, delay=False)
my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'))
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

def exiftool(path: str, dist: str):
    cmd = f"exiftool '-FileName<CreateDate' -d {sub('/*$', '', dist)}/%Y/%m/%Y-%m-%d_%H:%M:%S.%%e {path}"
    try:
        output = popen(cmd).read()
        app_log.info(output)
    except Exception as e:
        app_log.error(str(e))

class MyHandler(FileSystemEventHandler):
    def __init__(self, src, dist) -> None:
        self.src = src
        self.dist = dist
        super().__init__()

    def on_created(self, event):
        exiftool(self.src, self.dist)
        return super().on_created(event)

if __name__ == '__main__':
    [_, src, dist] = sys.argv
    observer = Observer()
    handler = MyHandler(src, dist)
    observer.schedule(handler, src, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()