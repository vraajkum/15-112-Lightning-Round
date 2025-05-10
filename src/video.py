################################################################################
# Combines clips into final video
################################################################################

import src.config as config
from src.utils import runCommand
import os
from PIL import Image, ImageDraw, ImageFont

################################################################################

def makeVideo(debug):
    print('Creating Title Image...\t', end='', flush=True)
    createTitleImage()
    print('Succeeded')

    print('Making Title Clip...\t', end='', flush=True)
    if makeTitleClip(debug):
        print('Succeeded')
    else:
        print('Failed')
        return
    
    print('Combining Clips...\t', end='', flush=True)
    if combineClips(debug):
        print('Succeeded')
    else:
        print('Failed')
        return
    
    print('Adding Music...\t\t', end='', flush=True)
    if addMusic(debug):
        print('Succeeded')
    else:
        print('Failed')

################################################################################

def createTitleImage():
    bgPath = os.path.join(config.assetDir, 'title-bg.png')
    outPath = os.path.join(config.finalDir, f'title.{config.imageFormat}')
    if os.path.exists(outPath):
        return
    
    fontPath = os.path.join(config.assetDir, 'Gobold Italic.otf')
    font = ImageFont.truetype(fontPath, size = 290) 
    color = (50, 83, 132)
    
    im = Image.open(bgPath).copy()
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.text((2180, 800), config.currSem, font=font, fill=color)
    im = im.resize((config.width, config.height))

    im.save(outPath, config.imageFormat)

def makeTitleClip(debug):
    inPath = os.path.join(config.finalDir, f'title.{config.imageFormat}')
    outPath = os.path.join(config.finalDir, f'title.{config.videoFormat}')
    if not os.path.exists(inPath):
        return False
    if os.path.exists(outPath):
        return True
    
    # specifies length of title (in seconds)
    titleLength = 3

    # Note: -pix_fmt yuv420p fixes a weird bug with Windows
    cmd = (f'ffmpeg -i {inPath} -r {config.fps} -t {titleLength} '
           f'-pix_fmt yuv420p -vf loop=-1:1 {outPath}')
    return runCommand(cmd, debug)

################################################################################

def combineClips(debug):
    textPath = os.path.join(config.finalDir, f'clipList.txt')
    makeClipList(textPath)

    outPath = os.path.join(config.finalDir, f'combined.{config.videoFormat}')
    if os.path.exists(outPath):
        return True
    
    # -safe 0 fixes a weird issue with the paths
    # -c copy can be omitted but speeds things up
    cmd = f'ffmpeg -f concat -safe 0 -i {textPath} -r 30 -c copy {outPath}'
    return runCommand(cmd, debug)

def makeClipList(path):
    titlePath = f'title.{config.videoFormat}'
    with open(path, 'w') as f:
        f.write(f"file '{titlePath}'\n")
        for file in os.listdir(config.overlaidVideoDir):
            path = os.path.join(config.overlaidVideoDir, file)
            relativePath = os.path.relpath(path, config.finalDir)
            f.write(f"file '{relativePath}'\n")

################################################################################

# Note: This might mess up the ending of the video
def addMusic(debug):
    musicPath = os.path.join(config.assetDir, f'music.mp3')
    inPath = os.path.join(config.finalDir, f'combined.{config.videoFormat}')
    outPath = os.path.join(config.finalDir, f'video.{config.videoFormat}')
    if not os.path.exists(inPath):
        return False
    if os.path.exists(outPath):
        return True
    
    cmd = (f'ffmpeg -i {inPath} '
           f'-stream_loop -1 -i {musicPath} '
           f'-shortest {outPath}')
    return runCommand(cmd, debug)

################################################################################