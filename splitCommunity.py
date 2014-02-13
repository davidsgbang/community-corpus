import glob
import os
import re

class SubtitleSplitter:
	def __init__(self, file):
		self.file = file

	def returnLines(self):
		with open(self.file, 'r') as fileText:
			rawData = fileText.read()
		rawData = re.sub(r'\r\n\r\n\r\n', r'\r\n\r\n', rawData)
		return self.extractLines(rawData)

	def extractLines(self, rawData):
		lines = rawData.split("\r\n\r\n")
		spokenLines = []
		monologue = ""
		for line in lines:
			processedLines = self.process2Lines(line.split("\r\n")[2:])
			if len(processedLines) == 2:
				spokenLines.append(self.trimLine(monologue + " " + processedLines[0]))
				monologue = ""
				if processedLines[1].find("|") > -1:
					spokenLines.append(self.trimLine(processedLines[1]))
				else:
					monologue += processedLines[1]
			else:
				if processedLines.find("|") > -1:
					spokenLines.append(self.trimLine(monologue + " " + processedLines))
					monologue = ""
				else:
					monologue += " " + processedLines
		return spokenLines
		

	def process2Lines(self, dupleLines):
		if len(dupleLines) == 2:
			if dupleLines[1][0] == "-":
				return dupleLines
		return " ".join(dupleLines)

	# trim the part where it's space and dash at the beginning
	def trimLine(self, line):
		return re.sub(r'\A(\s*-?\s+)', r'', line)

os.chdir("subtitles")
for episode in glob.glob("*.srt"):
	#print episode
	episodeSplitter = SubtitleSplitter(episode)
	#episodeSplitter.returnLines()
	for line in episodeSplitter.returnLines():
			print line
