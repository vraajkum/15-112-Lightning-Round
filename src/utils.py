import os, subprocess

# prints a horizontal line with the width of the terminal
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
            print()
            printLine()
            print(command)
            subprocess.run(command.split(), shell=True, check=True)
        else:
            # send stdout to devnull so nothing is printed
            subprocess.run(command.split(), shell=True, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        printLine()
        return True
    except:
        printLine()
        return False