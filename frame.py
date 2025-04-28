'''15-112 Frame Script

Parses CSV files and uses PIL to make frames.

Originally created by jxgong.
Updated by Vishant Raajkumar.

Dependencies:
  pip install pillow

Usage:
  see main.py
'''

import csv
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor

OUTPUT_DIR = 'frames'
WIDTH = 1920
HEIGHT = 1080
ASSET_DIR = 'assets'
OUTPUT_FORMAT = "png"

DRAGON = Image.open(os.path.join(ASSET_DIR, 'dragon.png'))
FONT_PATH = os.path.join(ASSET_DIR, 'Gobold Bold Italic.otf')
FONT = ImageFont.truetype(FONT_PATH, size = 96) 
SMALL_FONT = ImageFont.truetype(FONT_PATH, size = 42)
COLOR = (31, 82, 143)
LETTER_WIDTH = 55
MAX_WIDTH = WIDTH * 0.75 - 150

def writeFrame(id, title):
    title = title.lower()

    im = Image.new("RGBA", (WIDTH,HEIGHT))
    draw = ImageDraw.Draw(im, "RGBA")
    width = draw.textlength(title, font=FONT)
    if width > MAX_WIDTH:
        print(f'%{title} is too long, frame not created.')
        return False
    draw.rectangle([0, 800, 150+width+50, 930], fill = "white", outline = (0,0,0,0), width = 0)
    draw.text((165, 800), title, font=FONT, fill=COLOR)
    draw.text((0, 750), "112 S25", font=SMALL_FONT, fill=COLOR)
    draw.rectangle([0,800, 150, 930], fill=COLOR)
    im.paste(DRAGON, box = (15, 815))
    im = im.resize((1198, 720))

    outPath = os.path.join(OUTPUT_DIR, f'{id}.{OUTPUT_FORMAT}')
    im.save(outPath, OUTPUT_FORMAT)
    return True

def makeFrames(csvPath):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    terminalSize = os.get_terminal_size().columns

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        numFailed = 0
        total = 0

        print('-' * terminalSize)
        print('Creating frames:')
        print('-' * terminalSize)

        for line in csvReader:
            id, title, _, _, _ = line
            frameSuccess = writeFrame(id, title)
            if frameSuccess:
                print(f'Frame succeeded: {id}')
            else:
                print(f'Frame failed: {id}')
                numFailed += 1
            total += 1

    print('-' * terminalSize)
    print(f'Total: {total}')
    print(f'Failed: {numFailed}')
    print('-' * terminalSize)