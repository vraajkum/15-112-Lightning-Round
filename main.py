'''15-112 Lightning Round Script

A script to help make term project videos for 15-112 at CMU.
Downloads and trims student videos and creates a frame for the final video.

Originally created by Qiuwen "Owen" Fan and jxgong
Ported to python3 by Ben Owad.
Updated by Vishant Raajkumar.

Dependencies: pip install yt-dlp ffmpeg pillow

Usage:py main.py csv_file
where each line in csv_file has the format
vraajkum,coolTP,https://www.youtube.com/watch?v=dQw4w9WgXcQ,1:12,1:16
(ID, Project Name, Link, Start Time, End Time)
'''

import config
from clips import createClips
from video import makeVideo
import argparse, os, csv

def main(csvPath, debug):
    terminalSize = os.get_terminal_size().columns
    createMissingDirs()

    print('-' * terminalSize)
    print('Creating Clips')
    print(('-' * terminalSize) + '\n')
    clipSuccess = createClips(csvPath, debug)

    print('-' * terminalSize)
    print('Creating Video')
    print(('-' * terminalSize) + '\n')
    if not clipSuccess:
        print('Not all clips created, exiting')
        return
    makeVideo()
    print('-' * terminalSize)

def createMissingDirs():
    dirs = [config.fullVideoDir, config.trimmedVideoDir, config.frameDir,
            config.overlaidVideoDir]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', type=str, help='path to CSV file')
    parser.add_argument('--debug', action='store_true',
                        help='prints debug information')
    args = parser.parse_args()
    main(args.csvPath, args.debug)