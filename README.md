# 15-112 Lightning Round Script
This GitHub repository contains the files to make the Lighting Round video for 15-112 at CMU.

## About
The Lightning Round video contains clips of student term projects edited together with music.
Prior to this, we used multiple different scripts and we had many issues with getting them to run properly.
Therefore, I decided to combine the multiple scripts and update the code to be easier to understand.

The script takes in a CSV file with the project information and outputs the following for each project:
- the full project video (in the `full` folder)
- the trimmed clip (in the `trimmed` folder)
- a frame photo with the project name (in the `frames` folder)
- the clip overlaid with the frame (in the `overlaid` folder)

It also outputs the following to the `final` folder:
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
1. Have the leads share the Showcase Nomination Google Form with you. Make a copy of the form.
2. Make a new tab. Copy and paste the information into the tab.
3. Keep only the following columns: ID, Project Name, Link, Start Time, End Time
   - Remove all other columns
   - Remove the column names
   - Example: vraajkum,coolTP,https://www.youtube.com/watch?v=dQw4w9WgXcQ,1:12,1:16
4. Export as a CSV file.
5. Rename the file to something convenient like `lr.csv`.

### Running the Script
1. Download all of the files by either cloning the repository or downloading a zip file and unzipping it.
2. Place the CSV file within the outermost folder (the one containing [main.py](main.py)).
3. Open the file [src/config.py](src/config.py) and edit the settings.
   - Make sure you update `currSem` to your current semester!
   - I would recommend keeping the video settings the same.
5. Open a terminal in the outermost folder and enter the command `py main.py lr.csv` (replace `lr.csv` with the name of your CSV file)
   - Add `--debug` if you want the code to output debugging information (I don't recommend doing this when running for the first time)
6. The script will most likely fail for some projects. Keep running the code until it runs with no failures (see below for how to fix errors).

### Fixing Errors
Unfortunately, due to a variety of reasons (most often human error), the script will not run for certain projects.
If you run into any errors, make you run the script with the `--debug` flag since `yt-dlp`, `ffmpeg`, and `PIL` will most likely tell you the cause of the error. 
Here's how to debug different types of errors:

#### Download Errors
If a project video fails to download, it's most likely the result of one of the following issues:
- You don't have permission to access the video
- The video is hosted on an unsupported platform
- The link takes you to the wrong thing (most often a folder containing the video)

If you can access the video, then the easiest solution is to:
1. Manually download the video
2. Rename it to `id.mp4` (replace with the actual ID and correct video format)
3. Place it in the `full` folder.

If you don't have access, then contact the leads.
If they ask you to remove the project, then just delete the corresponding row in the CSV file.

#### Trim Errors
If a project video can't be trimmed properly, it's most likely because there's been some kind of data entry error.
You should try verifying the following:
- The start and end times are correctly formatted (should be mm:ss)
- The start and end times are actually within the duration of the video
- The start time is before the end time

If the code still doesn't work, then the easiest solution is to: 
1. Manually trim the video
2. Rename it to `id.mp4` (replace with the actual ID and correct video format)
3. Place it in the `trimmed` folder

#### Frame Creation Errors
The only reason why creating the frame photo can fail is that the project's title is too long.
In this case, you should edit the project title in the CSV file to be shorter (make sure it's still descriptive though).

#### Overlay Errors
This type of error should be very rare but if it does happen, the most common issue is that the clip wasn't trimmed properly.
You should verify that there are no trim errors, remove the clip from the `trimmed` folder (and the `overlaid` folder if it's there), and run the script again.

### Putting it all together
1. In the `final` folder, you should find the file `video.mp4` (the file format may change).
2. If the video isn't good enough (probably because the music cuts off abruptly), you will need to manually edit the video together.
   - You can find the overlaid clips in the `overlaid` folder, the title picture at `final/title.png`, and the music at [assets/music.mp3](assets/music.mp3).
   - You may be able to get away with just editing the video without the music, located at `final/combined.mp4`.
3. Once everything is satisfactory, upload the video to YouTube as unlisted and share with the leads!

## Future Development
If any future TAs want to contribute to this project, then you can fork the repository and make any edits you want.

One feature that I'd love to implement but am too lazy to figure out how to implement is a CSV validation script that makes sure everything is properly inputted.

If you need any assistance, have any questions, or want to let me know about any cool features you've implemented, you can contact me at vraajkum@andrew.cmu.edu and/or veekant@gmail.com.

## Credits
The portion of the script for downloading and trimming the clips was orignally written by Qiuwen "Owen" Fan and later ported to Python 3 by Ben Owad.

The portion of the script for creating the frame photos was originally written by Jason Gong.

The instructions were originally written by Asad Sheikh.

Massive thanks to everyone involved in making the previous script and instructions. 
This wouldn't be possible without all of their original contributions.
