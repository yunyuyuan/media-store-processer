from os import popen
from re import sub

time_format = '%Y/%m/%Y-%m-%d_%H-%M-%S.%%e'
time_format_p = '%Y/%m/%Y-%m-%d_%H-%M-%S%-c.%%e'
recursive = False

def get_cmd(tp: str, path: str, dist: str, cond: str, p: bool):
    return f"/usr/bin/vendor_perl/exiftool '-FileName<{tp}' -d {sub('/*$', '', dist)}/{time_format_p if p else time_format} {path}{' -r' if recursive else ''} {cond}"

def exiftool(path: str, dist: str, app_log = None):
    try:
        for [tp, cond, p] in [['CreateDate', '', False], ['FileModifyDate', " -if 'not $CreateDate'", True]]:
            output = popen(get_cmd(tp, path, dist, cond, p)).read()
            if app_log:
                app_log.info(output)
            else:
                print(output)
    except Exception as e:
        if app_log:
            app_log.error(str(e))
        else:
            print(str(e.with_traceback()))
