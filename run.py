from src import exiftool
import sys

if __name__ == '__main__':
    [_, src, dist] = sys.argv
    exiftool(src, dist)