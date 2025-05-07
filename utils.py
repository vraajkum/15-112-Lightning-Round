import os, subprocess

def printLine():
    terminalSize = os.get_terminal_size().columns
    print('-' * terminalSize)

def printHeader(text):
    printLine()
    print(text)
    printLine()

def runCommand(command, debug):
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