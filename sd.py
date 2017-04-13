import os
import urllib
import re
import youtube_dl
import subprocess
import requests
import time
from urllib.parse import urlparse
import easygui


def getYouUrl(song):
	queryString = urllib.parse.urlencode({"search_query" : song})
	htmlContent = urllib.request.urlopen("http://www.youtube.com/results?" + queryString)
	searchResults = re.findall(r'href=\"\/watch\?v=(.{11})', htmlContent.read().decode())
	url = "http://www.youtube.com/watch?v=" + searchResults[0]
	return url

def download(song, dir):
	url = getYouUrl(song)
	subprocess.call(['youtube-dl','-o',dir+'/%(title)s.(ext)s',"--extract-audio","--audio-format","mp3",url])	
	
def destinationFolder(file):
	i = 0
	while i < len(file):
		i+=1
		if file[i] == ".":
			return file[0:i]
	
	
def getMusic(fileLocation, playlist):
	i = 0
	songList = [line.strip() for line in open(fileLocation, 'r')]
	dir = os.path.dirname(fileLocation) + "\\" + destinationFolder(playlist)
	print (dir)
		
	if not os.path.exists(dir):
		os.mkdir(dir)
	
	for song in songList:
		download(song, dir)
		
def fileName(fileLocation):
	i = len(fileLocation) - 1
	while not fileLocation[i] == "\\" and i > 0:
		i -= 1
	return fileLocation[i+1:len(fileLocation)]

if __name__ == '__main__':
	dest = "C:\\Users\\jasmi_000\\Google Drive\\MUSIC\\Likes_Playlist\\"
	while True:
		#file = input("Enter file name: ")
		#fileLocation = dest + file
		fileLocation = easygui.fileopenbox()			
		file = fileName(fileLocation)
		print (file)
		if os.path.isfile(fileLocation):
			getMusic(fileLocation, file)
		else:
			print ("file not there")
		if not easygui.ynbox('Continue?', 'Title', ('Yes', 'No')):
			exit()


