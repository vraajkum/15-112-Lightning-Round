import config
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

def download(id, url, debug):
    outPath = os.path.join(config.fullVideoDir, f'{id}.{config.videoFormat}')
    if os.path.isfile(outPath):
        return True

    binary = f'{sys.executable} -m yt_dlp'
    cmd = binary + f' -f {config.videoFormat} -o {outPath} {url} --no-check-certificate'

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
    inPath = os.path.join(config.fullVideoDir, f'{id}.{config.videoFormat}')
    outPath = os.path.join(config.trimmedVideoDir, f'{id}.{config.videoFormat}')
    if not os.path.isfile(inPath):
        return False
    if os.path.isfile(outPath):
        return True

    startTime = mmssToSeconds(start)
    endTime = mmssToSeconds(end)
    command = f'''ffmpeg -i {inPath} -ss {startTime} -to {endTime} -an '''
    command += f'''-vf scale={config.width}:{config.height},pad={config.width}:{config.height}:(ow-iw)/2:(oh-ih)/2 {outPath}'''
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
    draw.rectangle([0, 800, 150+width+50, 930], fill = "white", outline = (0,0,0,0), width = 0)
    draw.text((165, 800), title, font=font, fill=color)
    draw.text((0, 750), config.currSem, font=smallFont, fill=color)
    draw.rectangle([0,800, 150, 930], fill=color)
    im.paste(dragon, box = (15, 815))

    outPath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    im.save(outPath, config.imageFormat)
    return True

def overlay(id, debug):
    framePath = os.path.join(config.frameDir, f'{id}.{config.imageFormat}')
    clipPath = os.path.join(config.trimmedVideoDir, f'{id}.{config.videoFormat}')
    outPath = os.path.join(config.overlaidVideoDir, f'{id}.{config.videoFormat}')
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