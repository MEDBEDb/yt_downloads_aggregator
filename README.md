# yt_downloads_aggregator
Download, maintain, hoard and update entire Youtube channels 

### How to run?

# 1A Compiled Binary (easy method)
Don't need to install anything, just download the repository and extract the files somewhere

# 1B (from source) Install required dependencies
1.1 Install Python https://www.python.org/downloads

1.2 Install yt-dlp https://github.com/yt-dlp/yt-dlp using A or B method

	1.2A Using Pip

		pip install -r requirements.txt or

	1.2B
		python -m pip install --upgrade yt-dlp or

	1.2C 
		Use the one from the /bin folder, just add it to your PATH


1.3 Verify it has been installed properly, run the following command: yt-dlp --version

Should return something like:  2022.05.18


# 2 Setup folder structure for your channels


A. YT Library folder structure: 

The script is reading the channel ID from the second string of the folder separated by space.
Currently there are 4 types of YT URLs supported: (Let me know if you find more)

Standard channels Examples, i.e.: 
a) https://www.youtube.com/user/_username_/videos
   https://www.youtube.com/user/partnersupport

b) https://www.youtube.com/c/'_channel-name_'/videos
   https://www.youtube.com/c/YouTubeCreators
   https://www.youtube.com/YouTubeCreators

or Legacy Channels Examples, just use the long channel ID, and the script will recognize it - i.e.:
c) https://www.youtube.com/channel/'_channel-hash-ID_'/videos
   https://www.youtube.com/channel/'_channel-hash-ID_'
   https://www.youtube.com/channel/UCUZHFZ9jIKrLroW8LcyJEQQ 

<RandomChosenName YouTubeCreators> <- folder with videos
RandomChosenName_(YouTubeCreators).txt <- text archive with already downloaded vids, no spaces, no special characters

For the first two each folder must contain two string: AnyGivenName username or AnyGivenName channel-name

	For example: FDF (FamilyDrivenFaith) 

For the later two, AnyGivenName HashID

	For example:  AOProductions (UCz4Qb-1lIttNRgB_lQDm6eA)

It will automatically create FDF_(FamilyDrivenFaith).txt and AOProductions_(UCz4Qb-1lIttNRgB_lQDm6eA).txt where all the already downloaded filenames will be stored.


B. Helper utilities
You can offload the videos later to an external hdd, and continue downloading only 
the new uploads using the txt archives


# 3 run the script 
A. From Source
Run the script using python aggregator.py -path "<Full path to download dir>" -sub "Subs,separated,by,comma" -format "format profile"
(eg.: "python aggregator.py -path "D:\YTDL\" -sub "en,ru,zh-Hans" -format "best[height<=480]")
For more media profiles - check https://github.com/yt-dlp/yt-dlp#format-selection-examples 

It will download all the newly uploaded videos for each channel, including subtitles and descriptions.
Also it will create archive.txt file, and update it with the downloaded indexes, so that at the next run it will not re-download already downloaded files.


B. Binary (easy) - make sure you add / update all your channels in the "data" folder
Run from terminal: 

Open bin/ folder

aggregator.exe  -path "D:\YTDL\" -sub "en,ru,zh-Hans" -format "best[height<=480]"


Video demo here: https://www.youtube.com/watch?v=gYtrAmYssA8 (a bit outdated)