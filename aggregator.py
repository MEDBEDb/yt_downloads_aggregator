import os, os.path
import subprocess
from subprocess import Popen, PIPE, CalledProcessError
import tempfile
import fnmatch
import argparse
import datetime
import sys

### TOFIX:
#WARNING: Unable to download webpage: <urlopen error [Errno 61] Connection refused> 
#TO compile into EXE pyinstaller --onefile -w aggregator.py
#ERROR: Unable to download webpage: <urlopen error [Errno 61] Connection refused> (caused by URLError(ConnectionRefusedError(61, 'Connection refused')))

# PRE_REQUISITES 
# pip install -U yt-dlp; #SRC https://github.com/yt-dlp/yt-dlp

parser = argparse.ArgumentParser(description='Specify your base dirrectory where all Youtube channels are saved')
parser.add_argument('string', help='Input dirrectory location', nargs='+')
args = parser.parse_args()
baseDir = ' '.join(args.string)
dirList = os.listdir(baseDir)
subtitleLanguages = 'en,ru,zh-Hans' # 'en,es,iw,ro,ru,zh-Hans'
# Download the best video with h264 codec, or the best video if there is no such video; # For other examples: https://github.com/yt-dlp/yt-dlp#format-selection-examples 
# mediaFormat = "(bv*[vcodec^=avc1]+ba) / (bv*+ba/b) " 
mediaFormat = "best[height<=480]"

# itterate through all the existing dirrectories and read index.txt files to get the base URL for each channel
for x in range(len(dirList)):
	if os.path.isdir(baseDir + dirList[x]):
		targetDir = (baseDir + dirList[x])
		numberOfMediaFilesInDirectoryBeforeDownload = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
		print("Starting downloading: " + dirList[x])
		print("Existing files: " + str(numberOfMediaFilesInDirectoryBeforeDownload)) 
		
		timeStamp = datetime.datetime.now()
		channelUrl = ""

		if (targetDir.__contains__("LgcyChn")):
			channelUrl = "https://www.youtube.com/channel/"+ str(targetDir.split(" ")[1]) + "/"
		else:
			channelUrl = "https://www.youtube.com/" + str(targetDir.split(" ")[1]) + "/videos/" 

		reportFile=open(targetDir + '/' + 'yt_downloads_aggregator_report_' + timeStamp.strftime("%Y_%m_%d-%H_%M_%S") + '.txt', 'a+', encoding='utf-8')
		reportFile.write(dirList[x] + ":")
		reportFile.write(" " + str(len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))) + " files before download")
		reportFile.write('\n')

		# Popen Docs https://docs.python.org/2/library/subprocess.html#subprocess.Popen 
		# To download comments (slow): --write-comments
		with Popen("yt-dlp --yes-playlist -v --newline --progress --restrict-filenames --write-auto-subs --write-subs --sub-langs " + subtitleLanguages + 
			" -f " + '"' + mediaFormat + '"' + " --recode-video mp4 --download-archive archive.txt --write-description -ciw " + channelUrl,
			stdout=PIPE, cwd=targetDir, bufsize=1, universal_newlines=True) as ytDlpProcess:
			for line in ytDlpProcess.stdout:
				print(line, end='') # process line here
				standardOutput = ytDlpProcess.stdout.read()
				# std_err = ytDlpProcess.stderr.read()

		if ytDlpProcess.returncode != 0:
			raise CalledProcessError(ytDlpProcess.returncode, ytDlpProcess.args)

		reportFile.write('\n')
		reportFile.write('Youtube-Dl OUTPUT: ')
		reportFile.write(standardOutput)
		reportFile.write('\n')

		# reportFile.write('Youtube-Dl ERRORS: ')
		# reportFile.write(std_err)
		# reportFile.write('\n')
		
		print("Finished downloading: " + dirList[x])
		numberOfFilesAfterDownloadCompleted = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
		print("Total number of files after update: " + str(numberOfFilesAfterDownloadCompleted))
		print("Files downloaded since the last update: " + str(numberOfFilesAfterDownloadCompleted - numberOfMediaFilesInDirectoryBeforeDownload)) 
		print('\n')
		reportFile.close()

	else:
		print(baseDir + dirList[x] + " not a directory")