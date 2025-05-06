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
from createClips import download, trim, createFrame, overlay
import argparse, os, csv

def main(csvPath, debug):
    terminalSize = os.get_terminal_size().columns
    createMissingDirs()

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failureInfo = dict()

        print(('-' * terminalSize) + '\n')
        for line in csvReader:
            processID(line, failureInfo, debug)
            print()

    displayFailureInfo(failureInfo)
    print('-' * terminalSize)

def createMissingDirs():
    dirs = [config.fullVideoDir, config.trimmedVideoDir, config.frameDir,
            config.overlaidVideoDir]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def processID(info, failureInfo, debug):
    id, title, url, start, end = info
    print(f'ID: {id}')

    print('Downloading...')
    if download(id, url, debug):
        print('\tSucceeded')
    else:
        print('\tFailed')
        failureInfo.get('Download', []).append(id)
        return

    print('Trimming...')
    if trim(id, start, end, debug):
        print('\tSucceeded')
    else:
        print("\tFailed")
        failureInfo.get('Trim', []).append(id)
        return

    print('Creating frame...')
    if createFrame(id, title):
        print('\tSucceeded')
    else:
        print("\tFailed")
        failureInfo.get('Frame', []).append(id)
        return

    print('Overlaying...')
    if overlay(id, debug):
        print('\tSucceeded')
    else:
        print("\tFailed")
        failureInfo.get('Overlay', []).append(id)
        return
    
def displayFailureInfo(failureInfo):
    if len(failureInfo) == 0:
        print('No failures!')
    else:
       for failureType in failureInfo:
           failures = failureInfo[failureType]
           print(f'{failureType}: {', '.join(failures)}') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', type=str, help='path to CSV file')
    parser.add_argument('--debug', action='store_true', help='prints debug information')
    args = parser.parse_args()
    main(args.csvPath, args.debug)