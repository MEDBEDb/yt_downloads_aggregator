import os, os.path
import subprocess
import fnmatch
import argparse

# Make sure there are only directorries in the source folder, i.e. no files
# Each dirrectory has to have a index.txt with a yt channel URL in it
# Run as python3 aggregator.py or python yt_downloads_aggregator.py

### TODO: 
# check if pip installed
# check if youtube-dl installed
# 	if not, install youtube-dl
# generate folders and index.txt files automatically (parse yotube channel names)
# improve progress visualization

# Set you root dir with all the channels to maintain, a folder per channel
#BaseDir = '/Volumes/Elements14Tb/YT/'

parser = argparse.ArgumentParser(description='Specify your base dirrectory where all Youtube channels are saved')
parser.add_argument('string', help='Input dirrectory location', nargs='+')
args = parser.parse_args()
BaseDir = ' '.join(args.string)
DirList = os.listdir(BaseDir) 

# itterate through all the existing dirrectories and read index.txt files to get the base URL for each channel
for x in range(len(DirList)):
	targetDir = BaseDir + DirList[x]
	num_files_per_dir = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
	print("Starting downloading: " + DirList[x])
	print("Existing files: " + str(num_files_per_dir)) 
	ReportFile=open(targetDir + '/' + 'yt_downloads_aggregator_report.txt','w')
	ReportFile.write(DirList[x] + ":")
	ReportFile.write(" " + str(len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))) + " files before download")
	ReportFile.write('\n')

  # initialize youtbube_dl process 
	YoutubeDlProcess = subprocess.Popen(['youtube-dl', '--write-auto-sub', '--sub-lang', 'en,es,iw,ro,ru,zh-Hans', 
		'-f', 'best', '--download-archive', 'archive.txt', '--write-description', '-citw', '-a', 'index.txt'], 
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
	num_files_per_dir_after_download_completes = len(fnmatch.filter(os.listdir(targetDir),'*.mp4'))
	print("Total number of files after update: " + str(num_files_per_dir_after_download_completes)) 
	print('\n')
ReportFile.close()
