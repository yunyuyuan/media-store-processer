import argparse
import datetime
import subprocess
import re
import os.path as path
import os
import shutil
import traceback

exif_path = '/usr/bin/vendor_perl/exiftool'
app_log = None

def get_args():
    parser = argparse.ArgumentParser(
                    prog = 'Media Refolder',
                    description = 'auto refold media files, using exiftool',
                    epilog = '')
    parser.add_argument('-s', '--src', required=True)
    parser.add_argument('-d', '--dist', required=True)
    parser.add_argument('-r', '--recursive', action='store_true', default=False)
    parser.add_argument('-c', '--copy', action='store_true', default=False)
    args = parser.parse_args()
    return args

def print_log(s):
    global app_log
    if app_log:
        app_log.info(s)
    else:
        print(s)

def run_command(command):
    process = subprocess.Popen(command, 
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    code = process.wait()
    out, err = process.communicate()
    log = f"[RUNNING]: {command}\nERROR: {err}\nOUTPUT: {out}"
    print_log(log)
    return out

def exiftool(_app_log = None):
    global app_log
    app_log = _app_log
    args = get_args()
    src = args.src
    dist = args.dist
    try:
        for filename in os.listdir(src):
            file_src = path.join(src, filename)
            file_src_quoted = "'" + file_src.replace("'", "'\\''") + "'"
            file_extension = os.path.splitext(filename)[1]

            formatted_date = None
            for time_key in ["CreateDate", "FileModifyDate"]:
                try:
                    original_format = '%Y:%m:%d %H:%M:%S'
                    create_date = run_command(f'{exif_path} -d "{original_format}" -{time_key} -s3 {file_src_quoted}').strip()
                    new_format = '%Y/%m/%Y-%m-%d_%H-%M-%S'
                    formatted_date = datetime.datetime.strptime(create_date, original_format).strftime(new_format)
                    break
                except:
                    pass
            
            if formatted_date is None:
                continue
            index = 0
            while 1:
                file_dist = path.join(dist, f"{formatted_date}{f'-{index}' if index else ''}{file_extension}")
                folder_dist = path.dirname(file_dist)
                if not path.exists(folder_dist):
                    os.makedirs(folder_dist)
                if path.exists(file_dist):
                    index += 1
                else:
                    # os.rename(file_src, file_dist)
                    shutil.move(file_src, file_dist)
                    print(f'[MOVE] {file_src} [TO] {file_dist}')
                    break
    except Exception as e:
        print_log('[Python error]: \n' + traceback.format_exc())
