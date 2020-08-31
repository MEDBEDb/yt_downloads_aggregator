# yt_downloads_aggregator
Download, maintain and update entire Youtube channels 


### How to use? 

# 1 Install required dependencies
1.1 Install Python 3 https://www.python.org/downloads/
1.2 Install Yt-Download lib, for windows follow 1.2.1 step, for nix - 1.2.2 (or 1.2.3 for both)
1.2.1 Windows: Go to https://yt-dl.org/downloads/ and find the ".exe" file
1.2.2 OS X and Linux 
a) Downlod the binary and place into /usr/local/bin folder
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
b) Make it executable
sudo chmod a+rx /usr/local/bin/youtube-dl
1.2.3 Using Pip
pip3 install -r requirements.txt

1.3 Verify it has been installed properly, run the following command: youtube-dl --version
Should return something like:  2020.07.28

# 2 Folder structure
Make sure all your channels are in the following format:

channel-name1/index.txt

channel-name2/index.txt

...

channel-nameN/index.txt



Index txt should contain the Youtube URL in the following format: 
https://www.youtube.com/user/<username>/videos
	or
https://www.youtube.com/channel/<channel-ID>/videos

# 3 run the script 
Run the script using "python3 aggregator.py /Path/to/your/channels/folder"

It will download all the newly uploaded videos for each channel, including subtitles and descriptions.
Also it will create archive.txt file, and update it with the downloaded indexes, so that at the next run it will not re-download already downloaded files.
