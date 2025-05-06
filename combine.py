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

def overlay(id, debug):
    framePath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    clipPath = os.path.join(config.trimmedVideoDir, f'{id}.{config.videoFormat}')
    outPath = os.path.join(config.overlayVideoDir, f'{id}.{config.videoFormat}')
    if not os.path.isfile(framePath) or not os.path.isfile(clipPath):
        return False
    if os.path.isfile(outPath):
        return True

    command = f"ffmpeg -i {clipPath} -i {framePath} -filter_complex [0][1]overlay=x=0:y=0 {outPath}"

    try:
        if debug:
            subprocess.run(command.split(), shell=True, check=True)
        else:
            subprocess.run(command.split(), shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False

def overlayClips(csvPath, debug):
    if not os.path.exists(config.overlayVideoDir):
        os.makedirs(config.overlayVideoDir)

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failed = set()
        total = 0

        print('Combining clips and frames:')
        print()

        for line in csvReader:
            id, _, _, _, _ = line
            print(f'ID: {id}')

            print('Combining...')
            if overlay(id, debug):
                print('\tSucceeded')
            else:
                print('\tFailed')
                failed.add(id)
            
            print()
            total += 1

    print(f'Total: {total}')
    print(f'Failed: {len(failed)}')
    if len(failed) > 0:
        print(f'Failed IDs: {', '.join(failed)}')