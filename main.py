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

import argparse, os
from dlTrim import downloadTrim
from frame import makeFrames
from combine import overlayClips

def main(csvPath, debug=False):
  terminalSize = os.get_terminal_size().columns
  print('-' * terminalSize)
  downloadTrim(csvPath, debug)
  print('-' * terminalSize)
  makeFrames(csvPath)
  print('-' * terminalSize)
  overlayClips(csvPath, debug)
  print('-' * terminalSize)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('csvPath', type=str, help='path to CSV file')
  parser.add_argument('--debug', action='store_true', help='prints debug information')
  args = parser.parse_args()
  main(args.csvPath, args.debug)