# source : http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
import random
import codecs

class CommunityMarkov:
	def __init__ (self, speaker, listener, interactions):
		self.name = speaker + " to " + listener
		self.sampleSize = ""
		self.db = {}
		for line in interactions:
			self.sampleSize += " " + line
		self.words = self.get_words()
		self.word_size = len(self.words)
		self.fillDB()

	def get_words(self):
		return self.sampleSize.split()

	def tuples(self):
		if len(self.words) < 5:
			return
		for i in range(len(self.words) - 5):
			yield (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3], self.words[i+4])

	def fillDB(self):
		for w1, w2, w3, w4, w5 in self.tuples():
			key = (w1, w2, w3, w4)
			if key in self.db:
				self.db[key].append(w5)
			else:
				self.db[key] = [w5]

	def generate_markov_text(self, size = 25):
		seed = random.randint(0, self.word_size-5)
		seed_word1, seed_word2, seed_word3, next_word = self.words[seed], self.words[seed+1], self.words[seed+2],self.words[seed+3]
		w1, w2, w3, w4 = seed_word1, seed_word2, seed_word3, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2, w3, w4 = w2, w3, w4, random.choice(self.db[(w1, w2, w3, w4)])
			gen_words.append(w2)
		return ' '.join(gen_words)