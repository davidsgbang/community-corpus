import glob
import os
import re
import pprint
from communityMarkov import CommunityMarkov

class SubtitleSplitter:
	def __init__(self, file):
		self.file = file

	def returnLines(self):
		with open(self.file, 'r') as fileText:
			rawData = fileText.read()
		rawData = re.sub(r'\r', r'', rawData)
		rawData = re.sub(r'\n\n\n', r'\n\n', rawData)
		#rawData = re.sub(r'\r+\n\r+\n(\r\n)*', r'\r\n\r\n', rawData)
		return self.extractLines(rawData)

	def extractLines(self, rawData):
		lines = rawData.split("\n\n")
		spokenLines = []
		monologue = ""
		for line in lines:
			if len(line.split("\n")) <= 2:
				continue
			processedLines = self.process2Lines(line.split("\n")[2:])
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
		if dupleLines == []:
			return ""
		dupleLines[0] = self.trimLine(dupleLines[0])
		# if the first line is the end of the line, then return two as separate lines
		if len(dupleLines) == 2:
			dupleLines[1] = self.trimLine(dupleLines[1])
			if dupleLines[0].find("|") > -1:
				return dupleLines
		return " ".join(dupleLines)

	# trim the part where it's space and dash at the beginning
	def trimLine(self, line):
		return re.sub(r'\A(\s*-?\s*)', r'', line)

class CharacterGraphMaker:
	def __init__(self):
		self.characterList = {}
		self.convoList = []

	def addEpisode(self, episode, episodeLines):
		self.episodeName = episode
		self.convoInEpisode = {}
		self.convoArr = []
		for line in episodeLines:
			self.getConversationSpeakers(line)
		
		for convo in sorted(self.convoInEpisode):
			self.convoList.append(self.convoInEpisode[convo])


	def getConversationSpeakers(self, line):

		spoken, characters, convoMarker = line.split("\t|")
		speaker, listeners = self.getSpeakerListeners(characters.lower().split(" "))	
		if speaker not in self.characterList:
			self.characterList[speaker] = Character(speaker)
		if convoMarker not in self.convoInEpisode:
			self.convoInEpisode[convoMarker] = [{
				"Speaker" : speaker,
				"Listeners" : " ".join(listeners),
				"Line" : spoken
			}]
		else:
			self.convoInEpisode[convoMarker].append( {
				"Speaker" : speaker,
				"Listeners" : " ".join(listeners),
				"Line" : spoken
			})
		for listener in listeners:
			self.characterList[speaker].spokenTo(listener, spoken)
		
	def getSpeakerListeners(self, characterList):
		speaker = characterList[0].lower()
		group = ["jeff", "britta", "abed", "troy", "pierce", "shirley", "annie"]
		#monologue
		if len(characterList) == 1:
			return speaker, ["self"]
		# more than one
		if len(characterList[1:]) != 1:
			listeners = characterList[1:]
			return speaker, listeners
		#dialogue
		else:
			return speaker, [characterList[1]]

	def getGraph(self):
		return self.characterList, self.convoList

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
		print "Speaker: " + self.name + "\n"
		#print self.interactions
		for char in self.interactions:
				print "\t" + char + "\n"
				for line in self.interactions[char]:
					print "\t\t" + line + "\n"
		print "\n"

os.chdir("Subtitles")
pp = pprint.PrettyPrinter(indent = 4)
characterGraph = CharacterGraphMaker()
for episode in sorted(glob.glob("*.srt")):
	episodeSplitter = SubtitleSplitter(episode)
	characterGraph.addEpisode(episode, episodeSplitter.returnLines())
graph, convoGraph = characterGraph.getGraph()

def getConvoSpeakerListener(speaker, listener):
	conversationList = []
	for conversation in convoGraph:
		for line in conversation:
			if line["Speaker"] == speaker and (listener in line["Listeners"].split()):
				conversationList.append(conversation)
				break

	return conversationList

def printConvo(convoList):
	for convo in convoList:
		for line in convo:
			print "Speaker: " + line["Speaker"] + " | Listeners: " + line["Listeners"]
			print "\t" + line["Line"]
		print "\n"

printConvo(getConvoSpeakerListener("pierce", "shirley"))



importantChar = ["all", "jeff", "annie", "shirley", "pierce", "troy", "abed", "britta", "slater", "chang", "duncan", "dean", "group"]
# speaker
for character in graph:
	if character not in importantChar:
		continue
	total = 0
	totalWord = 0
	# listener
	for interaction in graph[character].interactions.values():
		for line in interaction:
			totalWord += len(line.split())
		total += len(interaction)
	print character + ": " + str(total) + " lines | " + str(totalWord) + " words"

	for listener in graph[character].interactions.keys():
		if listener not in importantChar:
			continue

		lineNum = 0
		wordNum = 0
		for line in graph[character].interactions[listener]:
			lineNum += 1
			wordNum += len(line.split())
		print "\tto " + listener + ", " + character + " spoke " + str(wordNum / lineNum) + " words per each line" 
		print "\t\t Data:\n\t\t\tTotal Words = " + str(wordNum) + "\n\t\t\tTotal Lines = " + str(lineNum)
