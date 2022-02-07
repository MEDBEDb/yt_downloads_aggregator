# yt_downloads_aggregator
Download, maintain, hoard and update entire Youtube channels 

### How to run?

# 1A Compiled Binary (easy method)
Don't need to install anything, just download the repository and extract the files somewhere

# 1B (from source) Install required dependencies
1.1 Install Python https://www.python.org/downloads

1.2 Install yt-dlp https://github.com/yt-dlp/yt-dlp using A or B method

	1.2A Using Pip

		pip install -r requirements.txt 

	1.2B

		python -m pip install --upgrade yt-dlp


1.3 Verify it has been installed properly, run the following command: yt-dlp --version

Should return something like:  2022.02.04


# 2 Setup folder structure for your channels
The script is reading the channel ID from the second string of the folder separated by space.
Currently there are 4 types of YT URLs supported: (Let me know if you find more)

https://www.youtube.com/user/<username>/videos
https://www.youtube.com/c/<channel-name>/videos
https://www.youtube.com/channel/<channel-hash-ID>/videos
https://www.youtube.com/channel/<channel-hash-ID>

For the first two each folder must contain two string: AnyGivenName username or AnyGivenName channel-name
For example: FDF FamilyDrivenFaith 

For the later two, make sure to include LgcyChn as part of the first string: AnyGivenName HashID
For example:  AO&OProductions_LgcyChn UCz4Qb-1lIttNRgB_lQDm6eA



# 3 run the script 
A. Binary (easy) - make sure you add / update all your channels in the "data" folder
Run from terminal: 

Open bin/ folder

yt_downloads_aggregator_fotw.design.exe data/

B. From Source
Run the script using "python aggregator.py \Path\to\your\channels\folder\"



It will download all the newly uploaded videos for each channel, including subtitles and descriptions.
Also it will create archive.txt file, and update it with the downloaded indexes, so that at the next run it will not re-download already downloaded files.

Video demo here: https://youtu.be/DMfk8zgrsNI 