# This is used to process the subtitle.
# However, the subtitle needs to be supplemented by the 
class TextSplitter
	# initialize this shit. maybe return the processed shit? idk?
	def initialize(file)
		print startSplit(file)
	end

	def startSplit(file)
		rawData = File.read(file)
		# get rid of the double line that causes weird things.
		rawData.gsub!(/\r\n\r\n\r\n/,"\r\n\r\n")
		return extractLines(rawData)
	end

	def extractLines(rawData)
		# Split it up by subtitle occurance
		lines = rawData.split("\r\n\r\n")
		spokenLines = Array.new
		monologue = ""
		lines.each do |line|
			# for each subtitle occurance in the raw data, process the lines
			processedLines = processDupleLines(line.split("\r\n")[2..-1])
			# if there are two people speaking, then do additional processing
			if processedLines.size == 2
				# in the case of previous monologue, then first person ends the monologue.
				# so push in the monologue and the first line.
				spokenLines << "#{monologue} #{processedLines[0]}"
				monologue = ""
				# If the second line is not a monologue, then push it in
				# if not, then add to monologue and don't add just yet.
				if processedLines[1].include? "|"
					spokenLines << processedLines[1]
				else
					monologue << processedLines[1]
				end
			else
			# if it's a single line, and it's at the end of the monologue
			# then push it right in. but if it's still monologue
			# thenpush to monologue.
				if processedLines.include? "|"
					spokenLines << "#{monologue} #{processedLines}"
					monologue = ""
				else
					monologue << " #{processedLines}"
				end
			end
		end
		return spokenLines
	end

	# For duple lines, we want to make sure to combine two lines if they are spoken by the same character
	# However, if there is a dash, then two people talking, so don't combine
	def processDupleLines(dupleLines)
		# If there's two lines
		# if two people are talking (using "-" at the second line to indicate), then don't join
		# if not, join!
		if dupleLines.length == 2
			if dupleLines[1][0] == "-"
				return dupleLines
			end
		end
		return dupleLines.join(" ")
	end
end

# Look for every
Dir.chdir("subtitles")
Dir.glob("*.srt") do |file|
	#	puts file
		TextSplitter.new(file)
end