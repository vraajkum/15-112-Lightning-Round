import config
from utils import runCommand
import os
from PIL import Image, ImageDraw, ImageFont

def makeVideo(debug):
    createTitle()
    makeTitleClip(debug)
    combineClips(debug)
    addMusic(debug)

def createTitle():
    bgPath = os.path.join(config.assetDir, 'title-bg.png')
    outPath = os.path.join(config.finalDir, f'title.{config.imageFormat}')
    if os.path.exists(outPath):
        return
    
    fontPath = os.path.join(config.assetDir, 'Gobold Italic.otf')
    font = ImageFont.truetype(fontPath, size = 290) 
    color = (50, 83, 132)
    
    im = Image.open(bgPath).copy()
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.text((2210, 800), config.currSem, font=font, fill=color)
    im = im.resize((config.width, config.height))

    im.save(outPath, config.imageFormat)

def makeTitleClip(debug):
    inPath = os.path.join(config.finalDir, f'title.{config.imageFormat}')
    outPath = os.path.join(config.finalDir, f'title.{config.videoFormat}')
    if os.path.exists(outPath):
        return
    
    cmd = f'ffmpeg -i {inPath} -r 30 -t 3 -pix_fmt yuv420p -vf loop=-1:1 {outPath}'
    runCommand(cmd, debug)

def makeClipList():
    textPath = os.path.join(config.finalDir, f'clipList.txt')
    titlePath = f'title.{config.videoFormat}'
    with open(textPath, 'w') as f:
        f.write(f"file '{titlePath}'\n")
        for file in os.listdir(config.overlaidVideoDir):
            path = os.path.join(config.overlaidVideoDir, file)
            relativePath = os.path.relpath(path, config.finalDir)
            f.write(f"file '{relativePath}'\n")

def combineClips(debug):
    textPath = os.path.join(config.finalDir, f'clipList.txt')
    outPath = os.path.join(config.finalDir, f'combined.{config.videoFormat}')
    makeClipList()

    cmd = f'ffmpeg -f concat -safe 0 -i {textPath} -r 30 -c copy {outPath}'
    runCommand(cmd, debug)

def addMusic(debug):
    musicPath = os.path.join(config.assetDir, f'music.mp3')
    inPath = os.path.join(config.finalDir, f'combined.{config.videoFormat}')
    outPath = os.path.join(config.finalDir, f'video.{config.videoFormat}')

    cmd = f'ffmpeg -i {inPath} -stream_loop -1 -i {musicPath} '
    cmd += f'-shortest {outPath}'
    runCommand(cmd, debug)
    