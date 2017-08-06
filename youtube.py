import os
import urllib
import re
import subprocess
import requests
from colorshell import out

FFMPEG_BIN = r"C:\ffmpeg\bin"

def destinationFolder(file):
	i = 0
	while i < len(file):
		i+=1
		if file[i] == ".":
			return file[0:i]

def build_youtube_url(song):
	query_string = urllib.parse.urlencode({"search_query" : song})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	url = "http://www.youtube.com/watch?v=" + results[0]
	return url

def download(song):
	url = build_youtube_url(song)
	current_dir = os.path.dirname(os.path.realpath(__file__)) + r'/downloaded'
	subprocess.call(['youtube-dl', '-o',current_dir+'/%(title)s.(ext)s', "--extract-audio", "--ffmpeg-location", FFMPEG_BIN, "--audio-format", "mp3", url])

def get_music(filename):
	songs = [line.strip() for line in open(filename)]
	for song in songs:
		out.info('downloading {}'.format(song))
		download(song)

def main():
	if FFMPEG_BIN == "":
		out.error("please specify ffmpeg bin location")
	while True:
		filename = input("enter file name: ")
		if os.path.isfile(filename):
			out.info('grabing filename list from {}'.format(filename))
			get_music(filename)
			break
		else:
			out.info("file not there")

if __name__ == '__main__':
	main()
