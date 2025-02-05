import argparse
import datetime
import subprocess
import re
import glob
import os.path as path
import os
import pathlib
import shutil
import traceback

exif_path = '/usr/bin/vendor_perl/exiftool'
app_log = None

def get_args():
    parser = argparse.ArgumentParser(
                    prog = 'Media Refolder',
                    description = 'auto refold media files, using exiftool.',
                    epilog = '')
    parser.add_argument('-s', '--src', help='source dir.', required=True)
    parser.add_argument('-d', '--dist', help='source dir.', required=True)
    parser.add_argument('-f', '--format', help='ouput file format, default is %Y/%m/%Y-%m-%d_%H-%M-%S', default='%Y/%m/%Y-%m-%d_%H-%M-%S')
    parser.add_argument('-r', '--recursive', help='recursive process. default is false', action='store_true', default=False)
    parser.add_argument('-c', '--copy', help='do copy instead of moving. default is false', action='store_true', default=False)
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
    date_format = args.format
    do_copy = args.copy
    try:
        files = glob.glob(path.normpath(src) + ('/**/*.*' if args.recursive else '/*.*'), recursive=args.recursive)
        for file in files:
            file_src_quoted = "'" + file.replace("'", "'\\''") + "'"
            file_extension = pathlib.Path(file).suffix

            formatted_date = None
            for time_key in ["CreateDate", "FileModifyDate"]:
                try:
                    original_format = '%Y:%m:%d %H:%M:%S'
                    create_date = run_command(f'{exif_path} -d "{original_format}" -{time_key} -s3 {file_src_quoted}').strip()
                    formatted_date = datetime.datetime.strptime(create_date, original_format).strftime(date_format)
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
                    if do_copy:
                        shutil.copy2(file, file_dist)
                        print(f'[COPY] {file} [TO] {file_dist}')
                    else:
                        shutil.move(file, file_dist)
                        print(f'[MOVE] {file} [TO] {file_dist}')
                    break
    except Exception as e:
        print_log('[Python error]: \n' + traceback.format_exc())
