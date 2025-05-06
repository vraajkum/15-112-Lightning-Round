import config
from utils import mmssToSeconds, runCommand
import os, csv, sys
from PIL import Image, ImageDraw, ImageFont

def createClips(csvPath, debug):
    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failureInfo = dict()

        for line in csvReader:
            processID(line, failureInfo, debug)
            print()

    displayFailureInfo(failureInfo)
    return len(failureInfo) == 0

def processID(info, failureInfo, debug):
    id, title, url, start, end = info
    print(f'ID: {id}')

    vidFormat = config.videoFormat
    outPath = os.path.join(config.overlaidVideoDir, f'{id}.{vidFormat}')
    if os.path.isfile(outPath):
        print('Overlaid file found')
        return

    print('Downloading... ', end='', flush=True)
    if download(id, url, debug):
        print('Succeeded')
    else:
        print('Failed')
        failureInfo['Download'] = failureInfo.get('Download', []) + [id]
        return

    print('Trimming... ', end='', flush=True)
    if trim(id, start, end, debug):
        print('Succeeded')
    else:
        print("Failed")
        failureInfo['Trim'] = failureInfo.get('Trim', []) + [id]
        return

    print('Creating frame... ', end='', flush=True)
    if createFrame(id, title, debug):
        print('Succeeded')
    else:
        print("Failed")
        failureInfo['Frame'] = failureInfo.get('Frame', []) + [id]
        return

    print('Overlaying... ', end='', flush=True)
    if overlay(id, debug):
        print('Succeeded')
    else:
        print("Failed")
        failureInfo['Overlay'] = failureInfo.get('Overlay', []) + [id]
        return
    
def displayFailureInfo(failureInfo):
    if len(failureInfo) == 0:
        print('No failures!')
    else:
       print('Failures:')
       for failureType in ['Download', 'Trim', 'Frame', 'Overlay']:
           if failureType not in failureInfo:
               continue
           failures = failureInfo[failureType]
           print(f'{failureType}: {', '.join(failures)}') 

def download(id, url, debug):
    format = config.videoFormat
    outPath = os.path.join(config.fullVideoDir, f'{id}.{format}')
    if os.path.isfile(outPath):
        return True

    binary = f'{sys.executable} -m yt_dlp'
    cmd = binary + f' -f {format} -o {outPath} {url} --no-check-certificate'

    return runCommand(cmd, debug)

def trim(id, start, end, debug):
    format = config.videoFormat
    inPath = os.path.join(config.fullVideoDir, f'{id}.{format}')
    outPath = os.path.join(config.trimmedVideoDir, f'{id}.{format}')
    if not os.path.isfile(inPath):
        return False
    if os.path.isfile(outPath):
        return True

    startTime, endTime = mmssToSeconds(start), mmssToSeconds(end)
    w, h = config.width, config.height
    cmd = f'ffmpeg -i {inPath} -ss {startTime} -to {endTime} -an '
    cmd += f'-vf scale={w}:{h},pad={w}:{h}:(ow-iw)/2:(oh-ih)/2 {outPath}'
    
    return runCommand(cmd, debug)

def createFrame(id, title, debug):
    title = title.lower()
    dragon = Image.open(os.path.join(config.assetDir, 'dragon.png'))
    fontPath = os.path.join(config.assetDir, 'Gobold Bold Italic.otf')
    font = ImageFont.truetype(fontPath, size = 96) 
    smallFont = ImageFont.truetype(fontPath, size = 42)
    color = (31, 82, 143)
    maxWidth = config.width * 0.75 - 150

    im = Image.new('RGBA', (1920, 1080))
    draw = ImageDraw.Draw(im, 'RGBA')
    width = draw.textlength(title, font=font)
    if width > maxWidth:
        if debug:
            print(f'''"{title}" is too long, frame not created.''')
        return False
    draw.rectangle([0, 800, 150+width+50, 930], fill = "white",
                   outline = (0,0,0,0), width = 0)
    draw.text((165, 800), title, font=font, fill=color)
    draw.text((0, 750), '112 ' + config.currSem, font=smallFont, fill=color)
    draw.rectangle([0,800, 150, 930], fill=color)
    im.paste(dragon, box = (15, 815))
    im = Image.resize((config.width, config.height))

    outPath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    im.save(outPath, config.imageFormat)
    return True

def overlay(id, debug):
    imgFormat = config.imageFormat
    vidFormat = config.videoFormat

    framePath = os.path.join(config.frameDir, f'{id}.{imgFormat}')
    clipPath = os.path.join(config.trimmedVideoDir, f'{id}.{vidFormat}')
    outPath = os.path.join(config.overlaidVideoDir, f'{id}.{vidFormat}')
    if os.path.isfile(outPath):
        return True
    if not os.path.isfile(framePath) or not os.path.isfile(clipPath):
        return False

    cmd = f'ffmpeg -i {clipPath} -i {framePath} '
    cmd += f'-filter_complex [0][1]overlay=x=0:y=0 {outPath}'

    return runCommand(cmd, debug)