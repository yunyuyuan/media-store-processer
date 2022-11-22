from os import popen
from re import sub

def exiftool(path: str, dist: str, app_log = None):
    cmd = f"/usr/bin/vendor_perl/exiftool '-FileName<CreateDate' -d {sub('/*$', '', dist)}/%Y/%m/%Y-%m-%d_%H:%M:%S.%%e {path}"
    try:
        output = popen(cmd).read()
        if app_log:
            app_log.info(output)
        else:
            print(output)
    except Exception as e:
        if app_log:
            app_log.error(str(e))
        else:
            print(str(e.with_traceback()))
