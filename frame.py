'''15-112 Frame Script

Parses CSV files and uses PIL to make frames.

Originally created by jxgong.
Updated by Vishant Raajkumar.

Dependencies:
  pip install pillow

Usage:
  see main.py
'''

import config
import csv, os
from PIL import Image, ImageDraw, ImageFont

def writeFrame(id, title):
    title = title.lower()
    dragon = Image.open(os.path.join(config.assetDir, 'dragon.png'))
    fontPath = os.path.join(config.assetDir, 'Gobold Bold Italic.otf')
    font = ImageFont.truetype(fontPath, size = 96) 
    smallFont = ImageFont.truetype(fontPath, size = 42)
    color = (31, 82, 143)
    maxWidth = config.width * 0.75 - 150

    im = Image.new('RGBA', (config.width, config.height))
    draw = ImageDraw.Draw(im, 'RGBA')
    width = draw.textlength(title, font=font)
    if width > maxWidth:
        print(f'''"{title}" is too long, frame not created.''')
        return False
    draw.rectangle([0, 800, 150+width+50, 930], fill = "white", outline = (0,0,0,0), width = 0)
    draw.text((165, 800), title, font=font, fill=color)
    draw.text((0, 750), config.currSem, font=smallFont, fill=color)
    draw.rectangle([0,800, 150, 930], fill=color)
    im.paste(dragon, box = (15, 815))
    im = im.resize((1198, 720))

    outPath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    im.save(outPath, config.imageFormat)
    return True

def makeFrames(csvPath):
    if not os.path.exists(config.frameDir):
        os.makedirs(config.frameDir)

    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failed = []
        total = 0

        print('Creating frames:')
        print()

        for line in csvReader:
            id, title, _, _, _ = line
            frameSuccess = writeFrame(id, title)
            if frameSuccess:
                print(f'Frame succeeded: {id}')
            else:
                print(f'Frame failed: {id}')
                failed.append(id)
            total += 1

    print()
    print(f'Total: {total}')
    print(f'Failed: {len(failed)}')
    if len(failed) > 0:
        print(f'Failed IDs: {', '.join(failed)}')