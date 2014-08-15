import nltk
import random
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import defaultdict
stopwords = stopwords.words('english')
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
rhyme_entries = nltk.corpus.cmudict.entries()
syllable_guide = defaultdict( lambda: 1 )
for word, pronunciations in rhyme_entries:
	syllable_guide[word] = len([x for x in pronunciations if x[-1].isdigit() ])

poem = [
"You fill the room with sweet sensation",
"distracting bits of information",
"crowd the space where logic dwells",
"distorting sights and sounds and smells"
]

def is_common(word):
	return word in stopwords

def unconjugate(word):
	word = word.lower()
	word = stemmer.stem_word(word)
	word = lemmatizer.lemmatize(word)
	return word

def find_synonyms(word):
	synonyms = []
	syn_sets = wn.synsets(word)
	for syn_set in syn_sets:
		synonyms = synonyms + syn_set.lemma_names
	synonyms = [s.replace("_", " ") for s in synonyms if s != word]
	if len(synonyms) > 0:
		return synonyms
	else:
		return [word]

def reconjugate(word):
	return word #TODO

def rhymes(word1, word2):
	return True #TODO

def find_rhyme(word, rhymes):
	return rhymes[0] #TODO

def num_syllables(sentence):
	tokens = nltk.word_tokenize(sentence) 
	return sum( [ syllable_guide[word.lower()] for word in tokens ] )

def every_combination(choices):
	if len(choices) == 0:
		return ""
	if len(choices) == 1:
		return choices[0][:]
	combos = every_combination(choices[1:])
	extended_combos = []
	for choice in choices[0]:
		for combo in combos:
			extended_combos.append(choice + " " + combo)
	return extended_combos

last_words = []
synonymous_lines = []
for line in poem:
	words = nltk.word_tokenize(line)
	last_words.append(words[-1])
	synonymous_line = []
	for word in words:
		synonyms = [ word ]
		if not is_common(word):
			cleaned_word = unconjugate(word)
			synonyms = [reconjugate(x) for x in find_synonyms(cleaned_word)]
		else:
			synonyms = [word]
		synonymous_line.append(synonyms)
	synonymous_lines.append(synonymous_line)

for i in range(0, len(last_words)):
	for j in range(i + 1, len(last_words)):
		if rhymes(last_words[i], last_words[j]):
			possible_words_1 = synonymous_lines[i][-1]
			possible_words_2 = synonymous_lines[j][-1]
			for word in possible_words_1:
				rhyme = find_rhyme(word, possible_words_2)
				if rhyme:
					synonymous_lines[i][-1] = [word]
					synonymous_lines[j][-1] = [rhyme]
					break

for i in range(0, len(synonymous_lines)):
	target_syllables = num_syllables(poem[i])
	all_possible_sentences = every_combination(synonymous_lines[i])
	correctly_lengthed_sentences = []
	for sentence in all_possible_sentences:
		if num_syllables == target_syllables:
			correctly_lengthed_sentences.append(sentence)
	if len(correctly_lengthed_sentences) > 0:
		synonymous_lines[i] = random.choice(correctly_lengthed_sentences)
	else:
		synonymous_lines[i] = random.choice(all_possible_sentences)

print "ORIGINAL POEM"
for line in poem:
	print str(num_syllables(line)), '\t', line

print "\nSYNONYMOUS POEM"
for line in synonymous_lines:
	print str(num_syllables(line)), '\t', line