import glob
import os
import re
import pprint

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
		# if the first line is the end of the line, then return two as separate lines
		if len(dupleLines) == 2:
			if dupleLines[0].find("|") > -1:
				return dupleLines
		return " ".join(dupleLines)

	# trim the part where it's space and dash at the beginning
	def trimLine(self, line):
		return re.sub(r'\A(\s*-?\s+)', r'', line)

class CharacterGraphMaker:
	def __init__(self, episodeName, episodeLines):
		self.episodeName = episodeName
		self.characterList = {}
		for line in episodeLines:
			self.getConversationSpeakers(line)

	def getConversationSpeakers(self, line):
		spoken, characters = line.split("\t|")
		speaker, listeners = self.getSpeakerListeners(characters.split(" "))	
		if speaker not in self.characterList:
			self.characterList[speaker] = Character(speaker)
		for listener in listeners:
			self.characterList[speaker].spokenTo(listener, spoken)
		
	def getSpeakerListeners(self, characterList):
		speaker = characterList[0]
		group = ["Jeff", "Britta", "Abed", "Troy", "Pierce", "Shirley", "Annie"]
		#monologue
		if len(characterList) == 1:
			return speaker, ["self"]
		# more than one
		if len(characterList[1:]) != 1:
			listeners = characterList[1:]
			return speaker, listeners
		# spoken to the group
		if characterList[1] == "Group":
			listeners = [character for character in group if character != speaker]
			return speaker, listeners
		#dialogue
		else:
			return speaker, [characterList[1]]

	def getGraph(self):
		return self.characterList

class Character:
	def __init__(self, name):
		self.name = name
		self.interactions = {}

	def spokenTo(self, listener, line):
		#print listener
		if listener in self.interactions:
			self.interactions[listener].append(line)
		else:
			self.interactions[listener] = [line]

	def printChar(self):
		print self.name + "\n"
		print self.interactions
		print "\n"

os.chdir("Subtitles")
pp = pprint.PrettyPrinter(indent = 4)
'''
for episode in glob.glob("*.srt"):
	episodeSplitter = SubtitleSplitter(episode)
	characterGraph = CharacterGraphMaker(episode, episodeSplitter.returnLines())
	graph = characterGraph.getGraph()
	graph["Troy"].printChar()
'''
episodeSplitter = SubtitleSplitter("Community - 1x01 - Pilot.HDTV.FQM.en.srt")	
characterGraph = CharacterGraphMaker("Community - 1x01 - Pilot.HDTV.FQM.en.srt", episodeSplitter.returnLines())
graph = characterGraph.getGraph()
for char in graph:
	graph[char].printChar()