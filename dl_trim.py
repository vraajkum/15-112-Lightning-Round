'''15-112 Download/Trim Script

Downloads and trims student videos.

Originally created by Qiuwen "Owen" Fan and ported to python3 by Ben Owad.
Updated by Vishant Raajkumar.

Dependencies:
  pip install yt-dlp ffmpeg

Usage:
  see main.py
'''

import csv
import os, sys, subprocess

OUTPUT_FORMAT = 'mp4'
FULL_VIDEO_DIR = 'full'
TRIMMED_VIDEO_DIR = 'trimmed'
WIDTH = 1920
HEIGHT = 1080

def download(id, url):
    format = OUTPUT_FORMAT
    outPath = os.path.join(FULL_VIDEO_DIR, f'{id}.{format}')
    if os.path.isfile(outPath):
        return True

    binary = f'{sys.executable} -m yt_dlp'
    command = binary + f' -f {format} -o {outPath} {url} --no-check-certificate'

    try:
        subprocess.run(command.split(), shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False

def mmssToSeconds(s):
        seconds = 0
        for num in s.split(":"):
            seconds *= 60
            seconds += int(num)
        return seconds

def trim(id, start, end):
    inPath = os.path.join(FULL_VIDEO_DIR, f'{id}.{OUTPUT_FORMAT}')
    outPath = os.path.join(TRIMMED_VIDEO_DIR, f'{id}.{OUTPUT_FORMAT}')
    if os.path.isfile(outPath):
        return True

    startTime = mmssToSeconds(start)
    endTime = mmssToSeconds(end)
    command = f'''ffmpeg -i {inPath} -ss {startTime} -to {endTime} -an {outPath} -vf scale="{WIDTH}:{HEIGHT}"'''

    try:
        subprocess.run(command.split(), shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False

def downloadTrim(csvPath):
    if not os.path.exists(FULL_VIDEO_DIR):
        os.makedirs(FULL_VIDEO_DIR)
    if not os.path.exists(TRIMMED_VIDEO_DIR):
        os.makedirs(TRIMMED_VIDEO_DIR)

    terminalSize = os.get_terminal_size().columns

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        numFailed = 0
        total = 0

        print('-' * terminalSize)
        print('Downloading and trimming:')
        print('-' * terminalSize)
        print()

        for line in csvReader:
            id, _, link, start, end = line
            print(f'ID: {id}')

            print('Downloading...')
            if download(id, link):
                print('\tSucceeded')
            else:
                print('\tFailed')
                numFailed += 1
                continue

            print('Trimming...')
            if trim(id, start, end):
                print('\tSucceeded')
            else:
                print("\tFailed")
                numFailed += 1
                continue
            
            print()
            total += 1

    print('-' * terminalSize)
    print(f'Total: {total}')
    print(f'Failed: {numFailed}')