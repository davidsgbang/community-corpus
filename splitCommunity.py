import glob
import os
import re

class SubtitleSplitter:
	def __init__(self, file):
		print self.startSplit(file)

	def startSplit(self, file):
		with open(file, 'r') as fileText:
			rawData = fileText.read()
		return rawData

os.chdir("subtitles")
for episode in glob.glob("*.srt"):
	#print episode
	print SubtitleSplitter(episode)