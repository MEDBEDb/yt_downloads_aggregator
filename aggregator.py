import os, os.path
import subprocess
import fnmatch
import argparse
import datetime
import sys

# sys.stdout.buffer.write(data.encode('utf8'))
# setenv "PYTHONIOENCODING" "UTF-8"

### TODO: 
# generate folders and index.txt files automatically (parse yotube channel names)
# improve progress visualization

### TOFIX:
#WARNING: --title is deprecated. Use -o "%(title)s-%(id)s.%(ext)s" instead.
#WARNING: Unable to download webpage: <urlopen error [Errno 61] Connection refused>
#ERROR: Unable to download webpage: <urlopen error [Errno 61] Connection refused> (caused by URLError(ConnectionRefusedError(61, 'Connection refused')))

# PRE_REQUISITES
# python -m pip install --upgrade youtube-dlc

# YT-DLC SRC
# https://github.com/blackjack4494/yt-dlc


parser = argparse.ArgumentParser(description='Specify your base dirrectory where all Youtube channels are saved')
parser.add_argument('string', help='Input dirrectory location', nargs='+')
args = parser.parse_args()
BaseDir = ' '.join(args.string)
DirList = os.listdir(BaseDir)
#SubtitleLanguages = 'en,es,iw,ro,ru,zh-Hans'
SubtitleLanguages = 'en,ru,zh-Hans'

# itterate through all the existing dirrectories and read index.txt files to get the base URL for each channel
for x in range(len(DirList)):
	if os.path.isdir(BaseDir + DirList[x]):
		targetDir = (BaseDir + DirList[x])
		num_files_per_dir = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
		print("Starting downloading: " + DirList[x])
		print("Existing files: " + str(num_files_per_dir)) 
		TimeStamp = datetime.datetime.now()

		ReportFile=open(targetDir + '/' + 'yt_downloads_aggregator_report_' + TimeStamp.strftime("%Y_%m_%d-%H_%M_%S") + '.txt', 'a+', encoding='utf-8')
		ReportFile.write(DirList[x] + ":")
		ReportFile.write(" " + str(len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))) + " files before download")
		ReportFile.write('\n')

	  # initialize youtbube_dl process 
		YoutubeDlProcess = subprocess.Popen(['youtube-dlc', '--yes-playlist', '-v','--write-auto-sub', '--sub-lang', SubtitleLanguages, 
			'-f', 'best[height<=480]', '--download-archive', 'archive.txt', '--write-description', '-citw', '-a', 'index.txt'], 

# have video and audio separately
#			'-f', 'bestvideo[height<=480]+bestaudio/best[height<=480]', '--download-archive', 'archive.txt', '--write-description', '-citw', '-a', 'index.txt'], 

	    cwd=targetDir,
		bufsize=0,  # 0=unbuffered, 1=line-buffered, else buffer-size
		universal_newlines=True,
		close_fds=True,
	    #shell=True,
	    stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
		stdout,stderr = YoutubeDlProcess.communicate()

		ReportFile.write('\n')
		ReportFile.write('Youtube-Dl OUTPUT: ')
		print(stdout)
		ReportFile.write(stdout)
		ReportFile.write('\n')

		ReportFile.write('Youtube-Dl ERRORS: ')
		print(stderr)
		ReportFile.write(stderr)
		ReportFile.write('\n')
		print("Finished downloading: " + DirList[x])
		new_num_files = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
		print("Total number of files after update: " + str(new_num_files))
		print("Files downloaded since the last update: " + str(new_num_files - num_files_per_dir)) 
		print('\n')
		ReportFile.close()
	else:
		print(BaseDir + DirList[x] + " not a directory")