# yt_downloads_aggregator
Download, maintain and update entire Youtube channels 


### How to use? 

# 1 Install required dependencies
pip3 install -r requirements.txt

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
Update the BaseDIR containing all your folders (line 17)
BaseDir = '/path/to/your/folder'

Run the script using "python3 aggregator.py"

It will download all the newly uploaded videos for each channel, including subtitles and descriptions.
Also it will create archive.txt file, and update it with the downloaded indexes, so that at the next run it will not re-download already downloaded files.