import argparse
import subprocess
from re import sub
import shutil

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

def exiftool(app_log = None):
    args = get_args()
    try:
        for item in [
            {
                'tag': 'CreateDate',
                'cond': '',
                'format': '%Y/%m/%Y-%m-%d_%H-%M-%S.%%e',
            },{
                'tag': 'FileModifyDate',
                'cond': 'not $CreateDate',
                'format': '%Y/%m/%Y-%m-%d_%H-%M-%S%-c.%%e',
            },
        ]:
            process = subprocess.Popen(_generate_cmd(
                    src=args.src,
                    dist=args.dist,
                    tag=item['tag'],
                    format=item['format'],
                    cond=item['cond'],
                    copy=args.copy,
                    recursive=args.recursive
                ), 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
            code = process.wait()
            out, err = process.communicate()
            log = f"[out of <{item['tag']}>]:\n{err}\n{out}"
            if app_log:
                app_log.info(log)
            else:
                print(log)
    except Exception as e:
        if app_log:
            app_log.error('Python error:\n' + str(e))
        else:
            print(str(e))

def _generate_cmd(src: str, dist: str, tag: str, format: str, cond: str, copy: bool, recursive: bool):
    #exif_bin = shutil.which('exiftool')
    exif_bin = '/usr/bin/vendor_perl/exiftool'
    #if not exif_bin:
        #raise(Exception('exiftool binary not found!'))
    cmd = f"{exif_bin} '-FileName<{tag}'"
    cmd += f" -d {sub('/*$', '', dist)}/"
    cmd += format
    if copy:
        cmd += ' -o .'
    if recursive: 
        cmd += ' -r'
    if cond:
        cmd += f" -if '{cond}'"
    cmd += ' ' + src
    return cmd
