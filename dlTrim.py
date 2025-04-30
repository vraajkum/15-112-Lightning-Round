'''15-112 Download/Trim Script

Downloads and trims student videos.

Originally created by Qiuwen "Owen" Fan and ported to python3 by Ben Owad.
Updated by Vishant Raajkumar.

Dependencies:
  pip install yt-dlp ffmpeg

Usage:
  see main.py
'''
import config
import csv, os, sys, subprocess

def download(id, url, debug):
    format = config.videoFormat
    outPath = os.path.join(config.fullVideoDir, f'{id}.{format}')
    if os.path.isfile(outPath):
        return True

    binary = f'{sys.executable} -m yt_dlp'
    command = binary + f' -f {format} -o {outPath} {url} --no-check-certificate'

    try:
        if debug:
            subprocess.run(command.split(), shell=True, check=True)
        else:
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

def trim(id, start, end, debug):
    inPath = os.path.join(config.fullVideoDir, f'{id}.{config.videoFormat}')
    outPath = os.path.join(config.trimmedVideoDir, f'{id}.{config.videoFormat}')
    if not os.path.isfile(inPath):
        return False
    if os.path.isfile(outPath):
        return True

    startTime = mmssToSeconds(start)
    endTime = mmssToSeconds(end)
    command = f"ffmpeg -i {inPath} -ss {startTime} -to {endTime}-an {outPath}"
    command += f'''-vf scale="{config.width}:{config.height}"'''

    try:
        if debug:
            subprocess.run(command.split(), shell=True, check=True)
        else:
            subprocess.run(command.split(), shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False

def downloadTrim(csvPath, debug):
    if not os.path.exists(config.fullVideoDir):
        os.makedirs(config.fullVideoDir)
    if not os.path.exists(config.trimmedVideoDir):
        os.makedirs(config.trimmedVideoDir)

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failed = set()
        total = 0

        print('Downloading and trimming:')
        print()

        for line in csvReader:
            id, _, link, start, end = line
            print(f'ID: {id}')

            print('Downloading...')
            if download(id, link, debug):
                print('\tSucceeded')
            else:
                print('\tFailed')
                failed.add(id)

            print('Trimming...')
            if trim(id, start, end, debug):
                print('\tSucceeded')
            else:
                print("\tFailed")
                failed.add(id)
            
            print()
            total += 1

    print(f'Total: {total}')
    print(f'Failed: {len(failed)}')
    if len(failed) > 0:
        print(f'Failed IDs: {', '.join(failed)}')