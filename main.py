'''15-112 Lightning Round Script

A script to help make term project videos for 15-112 at CMU.
Downloads and trims student videos and creates a frame for the final video.

Originally created by Qiuwen "Owen" Fan and jxgong
Ported to python3 by Ben Owad.
Updated by Vishant Raajkumar.

Dependencies:
  pip install yt-dlp ffmpeg pillow

Usage:
  py main.py csv_file
  where each line in csv_file has the format
  vraajkum,coolTP,https://www.youtube.com/watch?v=dQw4w9WgXcQ,1:12,1:16
  (ID, Project Name, Link, Start Time, End Time)
'''

import argparse
from dl_trim import downloadTrim
from frame import makeFrames

def main(csvPath):
    downloadTrim(csvPath)
    makeFrames(csvPath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', type=str)
    args = parser.parse_args()
    main(args.csvPath)