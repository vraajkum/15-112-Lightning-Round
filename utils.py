import subprocess

def mmssToSeconds(s):
    seconds = 0
    for num in s.split(":"):
        seconds *= 60
        seconds += int(num)
    return seconds

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