import subprocess
from re import sub
import shutil

recursive = False
copy = True

def exiftool(path: str, dist: str, app_log = None):
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
            process = subprocess.Popen(generate_cmd(
                    src=path,
                    dist=dist,
                    tag=item['tag'],
                    format=item['format'],
                    cond=item['cond'],
                    copy=copy,
                    recursive=recursive
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

def generate_cmd(src: str, dist: str, tag: str, format: str, cond: str, copy: bool, recursive: bool):
    exif_bin = shutil.which('exiftool')
    if not exif_bin:
        raise(Exception('exiftool binary not found!'))
    cmd = f"{exif_bin} '-FileName<{tag}'"
    cmd += f" -d {sub('/*$', '', dist)}/{format}"
    if copy:
        cmd += ' -o .'
    if recursive: 
        cmd += ' -r'
    if cond:
        cmd += f" -if '{cond}'"
    cmd += ' ' + src
    return cmd
