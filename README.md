# yt_downloads_aggregator
Download, maintain, hoard and update entire Youtube channels 

### How to run?

# 1A Compiled Binary (easy method)
Don't need to install anything, just download the repository and extract the files somewhere

# 1B (from source) Install required dependencies
1.1 Install Python https://www.python.org/downloads/

1.2 Install Yt-DLC https://github.com/blackjack4494/yt-dlc using A or B method

	1.2A Using Pip

		pip install -r requirements.txt 

	1.2B

		python -m pip install --upgrade youtube-dlc


1.3 Verify it has been installed properly, run the following command: youtube-dlc --version

Should return something like:  2020.11.11-3


# 2 Setup folder structure for your channels
Make sure each channel has an index.txt file with the URL pointing to Youtube.

randomChannel/index.txt

randomChanne2/index.txt

...

randomChanneX/index.txt


Index txt should contain the Youtube URL in the following format: 
https://www.youtube.com/user/<username>/videos
	or
https://www.youtube.com/channel/<channel-ID>/videos

# 3 run the script 
A. Binary (easy) - make sure you add / update all your channels in the "data" folder
Run from terminal: yt_downloads_aggregator_fotw.design.exe data/

B. From Source
Run the script using "python aggregator.py \Path\to\your\channels\folder\"



It will download all the newly uploaded videos for each channel, including subtitles and descriptions.
Also it will create archive.txt file, and update it with the downloaded indexes, so that at the next run it will not re-download already downloaded files.

Video demo here: https://youtu.be/DMfk8zgrsNI 