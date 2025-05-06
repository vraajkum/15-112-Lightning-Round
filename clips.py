import config
import os, csv, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

def createClips(csvPath, debug):
    with open(csvPath, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        failureInfo = dict()

        for line in csvReader:
            processID(line, failureInfo, debug)
            print()

    displayFailureInfo(failureInfo)

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

def download(id, url, debug):
    format = config.videoFormat
    outPath = os.path.join(config.fullVideoDir, f'{id}.{format}')
    if os.path.isfile(outPath):
        return True

    binary = f'{sys.executable} -m yt_dlp'
    cmd = binary + f' -f {format} -o {outPath} {url} --no-check-certificate'

    try:
        if debug:
            print(cmd)
            subprocess.run(cmd.split(), shell=True, check=True)
        else:
            subprocess.run(cmd.split(), shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False

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
    command = f'ffmpeg -i {inPath} -ss {startTime} -to {endTime} -an '
    command += f'-vf scale={w}:{h},pad={w}:{h}:(ow-iw)/2:(oh-ih)/2 {outPath}'
    try:
        if debug:
            print(command)
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

def createFrame(id, title):
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
    draw.rectangle([0, 800, 150+width+50, 930], fill = "white",
                   outline = (0,0,0,0), width = 0)
    draw.text((165, 800), title, font=font, fill=color)
    draw.text((0, 750), config.currSem, font=smallFont, fill=color)
    draw.rectangle([0,800, 150, 930], fill=color)
    im.paste(dragon, box = (15, 815))

    outPath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    im.save(outPath, config.imageFormat)
    return True

def overlay(id, debug):
    imgFormat = config.imageFormat
    vidFormat = config.videoFormat

    framePath = os.path.join(config.frameDir, f'{id}.{imgFormat}')
    clipPath = os.path.join(config.trimmedVideoDir, f'{id}.{vidFormat}')
    outPath = os.path.join(config.overlaidVideoDir, f'{id}.{vidFormat}')
    if not os.path.isfile(framePath) or not os.path.isfile(clipPath):
        return False
    if os.path.isfile(outPath):
        return True

    command = f'ffmpeg -i {clipPath} -i {framePath} '
    command += f'-filter_complex [0][1]overlay=x=0:y=0 {outPath}'

    try:
        if debug:
            subprocess.run(command.split(), shell=True, check=True)
        else:
            subprocess.run(command.split(), shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except:
        return False