# 15-112 Lightning Round Script
This GitHub repository contains the files to make the Lighting Round video for 15-112 at CMU.

## About
The Lightning Round video contains clips of student term projects edited together with music.
Prior to this, we used multiple different scripts and we had many issues with getting them to run properly.
Therefore, I decided to combine the multiple scripts and update the code to be easier to understand.

The script takes in a CSV file with the project information and outputs the following for each project:
- the full project video
- the trimmed clip
- a frame photo with the project name
- the clip overlaid with the frame

It also outputs the following:
- the title photo and clip
- all clips combined without music
- all clips combined with music

## Dependencies
You will need [Python 3.12+](https://www.python.org/downloads/) installed on your computer.
I've only tested Python 3.12.10 so I'm not sure if the script works with other versions.

You'll also need the Python modules yt-dlp and PIL.
The following commands can be entered into the terminal to install them:
```
py -m pip install yt-dlp
py -m pip install pillow
```
You may need to replace `py` with `python`, `python3`, or the path to the folder containing your Python executable.

Lastly, you'll need to install ffmpeg.
The installation depends on the platform:
- Windows - Download the file "ffmpeg-git-full.7z" from [this link](https://www.gyan.dev/ffmpeg/builds/) and unzip
- Mac - Enter the command `brew install ffmpeg` in the terminal or download from [this link](https://evermeet.cx/ffmpeg/) and unzip
If you manually install ffmpeg, add the folder containing the ffmpeg executable to your PATH variable (if stuck, [here's](https://www.java.com/en/download/help/path.html) a good resource).

## Usage
So you've been assigned to make the Lighting Round video... 😭  
Here's what to do:

### Making the CSV File
1. Have the Leads share the Showcase Nomination Google Form with you. Make a copy of the form.
2. Make a new tab. Copy and paste the information into the tab.
3. Keep only the following columns: ID, Project Name, Link, Start Time, End Time
   - Remove all other columns
   - Remove the column names
4. Export as a CSV file.
5. Rename the file to something convenient like `lr.csv`.

### Running the Script
1. Download the script by


Originally created by Qiuwen "Owen" Fan and Jason Gong.
Ported to python3 by Ben Owad.
Updated by Vishant Raajkumar.

Dependencies: pip install yt-dlp ffmpeg pillow

Usage:py main.py csv_file
where each line in csv_file has the format
vraajkum,coolTP,https://www.youtube.com/watch?v=dQw4w9WgXcQ,1:12,1:16
(ID, Project Name, Link, Start Time, End Time)
'''
