################################################################################
# Main file (see README.md for instructions on how to run)
################################################################################

import src.config as config
from src.utils import printLine, printHeader
from src.clips import createClips
from src.video import makeVideo
import argparse, os

################################################################################

def main(csvPath, debug):
    createMissingDirs()

    printHeader('Creating Clips')
    clipSuccess = createClips(csvPath, debug)

    printHeader('Creating Video')
    if clipSuccess:
        makeVideo(debug)
    else:
        print('Not all clips created, exiting')
    printLine()

def createMissingDirs():
    dirs = [config.fullVideoDir, config.trimmedVideoDir, config.frameDir,
            config.overlaidVideoDir, config.finalDir]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csvPath', type=str, help='path to CSV file')
    parser.add_argument('--debug', action='store_true',
                        help='prints debug information')
    args = parser.parse_args()
    main(args.csvPath, args.debug)

################################################################################