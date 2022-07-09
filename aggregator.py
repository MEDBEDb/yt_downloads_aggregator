#!/usr/bin/env python3

import os, os.path
import subprocess
from subprocess import Popen, PIPE, CalledProcessError
import tempfile
import fnmatch
import argparse
import datetime
import sys
import shutil
import random
import pdb 
import glob
import re

"""
***********************
******Debugging:*******
***********************
Use PDB for debugging purposes, just place the line anywhere:
https://docs.python.org/3/library/functions.html
pdb.set_trace()
p dir(<obj>)

To download comments (slow): --write-comments
Debug1: yt-dlp --yes-playlist -v --newline --progress --restrict-filenames --write-auto-subs --write-subs --sub-langs  "en,ru,zh-Hans" -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b" --recode-video mp4 --download-archive archive.txt --write-description -ciw -a index.txt
Debug1: yt-dlp --yes-playlist -v --newline --progress --restrict-filenames --embed-thumbnail --write-thumbnail --embed-metadata --write-auto-subs --write-subs --sub-langs  "en,ru,zh-Hans" -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b" --recode-video mp4 --part --write-playlist-metafiles --download-archive archive.txt --write-description -ciw -a index.txt 

WITH METADATA
with Popen("yt-dlp --yes-playlist -v --newline --progress --restrict-filenames --embed-thumbnail --embed-metadata --write-thumbnail --write-auto-subs --write-subs --sub-langs " + subtitleLanguages + " -f " + '"' + mediaFormat + '"' + " --recode-video mp4 --part --write-playlist-metafiles --download-archive archive.txt --write-description -ciw "  \"something with spaces\"" + channelUrl
"""


#TODO: to be tested, after folder naming refactoring
def offload(input, outut):
	destination_dir = outut
	for dir_name in glob.iglob(input + '*', recursive=True):
		if os.path.isdir(dir_name):
			for subdir_name in glob.iglob(dir_name + '*', recursive=True):
				print("\n")
				print("Moving: " + str(subdir_name))
				for file_name in glob.iglob(subdir_name + '/**/*.*', recursive=True):
					channel_name_from_dir = subdir_name.split("\\")[2]
					print("File: " + str(file_name))
					if os.path.isfile(os.path.join(destination_dir + channel_name_from_dir + "\\", file_name)):
						shutil.copy(file_name,  destination_dir + channel_name_from_dir + "\\") # , dirs_exist_ok=True
						os.remove(file_name)
					else: 
						shutil.move(file_name,  destination_dir + channel_name_from_dir + "\\")

#TODO: to be tested, after folder naming refactoring
def generate_missing_dirs_for_present_archives():
	print("\n")
	# for file_name in glob.iglob('Desktop/**/*.txt', recursive=True):
	for file_name in glob.iglob(baseDir + '*.txt', recursive=True):
		pattern_for_Id = r"\((.*?)\)"
		stringId = re.search(pattern_for_Id, file_name)
		channelUrlId = stringId.group(1)
		channelShortName = file_name.split("\\")[2].split("(")[0][:-1]
		channel_dir_name = baseDir + channelShortName + " (" + channelUrlId + ")" 
		#TODO - check others
		
		for dir_name in glob.iglob(baseDir + '*', recursive=True):
			if os.path.isdir(dir_name):
				for subdir_name in glob.iglob(dir_name + '*', recursive=True):
					if not os.path.exists(channel_dir_name):
						os.makedirs(channel_dir_name)

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def aggregate(argv):

	parser = argparse.ArgumentParser(description='Specify your base dirrectory where all Youtube channels will be saved')
	parser.add_argument('-path', help='Input dirrectory location',type=dir_path)
	parser.add_argument('-sub', help='Subtitles to be downloaded', nargs='?')
	parser.add_argument('-format', help='Encoding format, for more details see https://github.com/yt-dlp/yt-dlp#format-selection-examples', nargs='?')
	parser.add_argument('-offload', help='Run Offload utility, will move all your downloaded videos to a specified location (could be an external HDD)', nargs='+')
	args = parser.parse_args()

	#If no args are provided, print help and exit
	if len(sys.argv) < 2 and argv[0] not in '-offload': 
	    print("Path: 1 - Not enough arguments")
	    parser.print_help()
	elif len(argv) >= 2 and argv[0] in '-offload':
		print("Path: 2 - Offloading files")
		pdb.set_trace()
		inputDir = argv[1]
		outputDir = argv[2]
		# offload(inputDir, outputDir) #TO BE TESTED
	elif argv[0] not in '-offload':
		print("Path: 3 - Preparing to start the downloader")
		baseDir = args.path
		subtitleLanguages = args.sub 
		mediaFormat = args.format 
		dirList = os.listdir(baseDir)

		# itterate through all the existing dirrectories and read 2nd argument to get the base URL for each channel
		for x in range(len(dirList)):
			if os.path.isdir(os.path.join(baseDir + dirList[x])) and len(dirList[x].split(" "))>1:
				targetDir = (baseDir + dirList[x])
				channelName = str(targetDir).split(" ")[0]
				channelUrlId = re.sub(r"\(|\)", "", str(targetDir).split(" ")[1])
				timeStamp = datetime.datetime.now()
				channelTextArchive =  channelName + "_" + "(" + channelUrlId + ")" + ".txt"
				numberOfMediaFilesInDirectoryBeforeDownload = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))

				print("Path: 3a - Downloading channel: " + dirList[x])
				print("Existing files: " + str(numberOfMediaFilesInDirectoryBeforeDownload)) 

				pattern_for_Legacy_Id = r"[0-9A-Za-z_-]{23}[AQgw]$"
				if (re.match(pattern_for_Legacy_Id, channelUrlId)):
					channelUrl = "https://www.youtube.com/channel/" + channelUrlId + "/"
				else: 
					channelUrl = "https://www.youtube.com/" + channelUrlId + "/videos/"

				command = ("yt-dlp --yes-playlist -v --newline --progress --restrict-filenames --no-hls-use-mpegts --embed-thumbnail" 
				+ " --write-thumbnail --write-auto-subs --write-subs --sub-langs " + subtitleLanguages + " -f " + '"' + mediaFormat + '"' 
				+ " --recode-video mp4 --part --write-playlist-metafiles --download-archive " + channelTextArchive 
				+ " --write-description -ciw " + channelUrl)

				reportFile=open(targetDir + '/' + 'yt_downloads_aggregator_report_' + timeStamp.strftime("%Y_%m_%d-%H_%M_%S") + '.txt', 'a+', encoding='utf-8')
				reportFile.write(dirList[x] + ":")
				reportFile.write(" " + str(len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))) + " files before download")
				reportFile.write('\n')

				try:
					# Popen Docs https://docs.python.org/2/library/subprocess.html#subprocess.Popen 
					with Popen(command, shell=True, stdout=PIPE, cwd=targetDir, bufsize=1, universal_newlines=True) as ytDlpProcess:
						for line in ytDlpProcess.stdout:
							print(line, end='') # process line here
							reportFile.write(line)
							standardOutput = ytDlpProcess.stdout.read()
							reportFile.write(standardOutput)
							# std_err = ytDlpProcess.stderr.read()
							# reportFile.write(std_err)
							numberOfMediaFilesInDirectoryAfterDownload = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))

						if ytDlpProcess.returncode != 0:
							raise CalledProcessError(ytDlpProcess.returncode, ytDlpProcess.args)
							#raise ExtractorError

				except BaseException as e:
						summary_report=open(baseDir + "/" + '_summary_report' + timeStamp.strftime("%Y_%m_%d") + '.txt', 'a+', encoding='utf-8')
						summary_report.write('\n')
						summary_report.write("Dowload dir: " + dirList[x])
						summary_report.write('\n')
						summary_report.write("Channel URL: " + channelUrl)
						summary_report.write('\n')
						summary_report.write("Existing files (before download): " + str(numberOfMediaFilesInDirectoryBeforeDownload)) 
						summary_report.write('\n')
						summary_report.write("Total number of files after update: " + str(numberOfMediaFilesInDirectoryAfterDownload))
						summary_report.write('\n')
						summary_report.write("Files downloaded since the last update: " + str(numberOfMediaFilesInDirectoryAfterDownload - numberOfMediaFilesInDirectoryBeforeDownload)) 
						summary_report.write('\n')
						summary_report.write("Debug Command: " + str(e.args))
						summary_report.write('\n')
						summary_report.write('\n')
						pass 

				finally:
					numberOfFilesAfterDownloadCompleted = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))

					reportFile.write('\n')
					reportFile.write('Youtube-Dl OUTPUT: ')
					reportFile.write(standardOutput)
					reportFile.write('\n')

					# reportFile.write('Youtube-Dl ERRORS: ')
					# reportFile.write(std_err)
					# reportFile.write('\n')
					
					print("Finished downloading: " + dirList[x])
					print("Total number of files after update: " + str(numberOfFilesAfterDownloadCompleted))
					print("Files downloaded since the last update: " + str(numberOfFilesAfterDownloadCompleted - numberOfMediaFilesInDirectoryBeforeDownload)) 
					print('\n')
					reportFile.close()
			elif(os.path.isdir(os.path.join(baseDir + dirList[x])) and len(dirList[x].split(" "))<2): #TOFIX len(dirList)<1 )
				print("Something went wrong. No valid youtube channels found. Check your folders structure. "
					+ "Please create empty folders in the format: <RandomChosenName validYoutubeChanelName>")
			else:
				# print("Path: 3b - Skipping the files, only taking the dirrectories from the base_dir. Here be dragons...")
				# print(baseDir + dirList[x] + " not a directory")
				continue 
	else:
		print("Path: 4 - Houston, we've got a problem...")
		parser.print_help()

if __name__ == '__main__':
    aggregate(sys.argv[1:])