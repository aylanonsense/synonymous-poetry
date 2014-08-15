import urllib2, json

key = "heVLNQppoMMLfUZQpRMz"

def getSynonyms(word):
	url = "http://thesaurus.altervista.org/thesaurus/v1?key="+key+"&word="+word+"&language=en_US&output=json"
	try:
		feed = urllib2.urlopen(url)
		text_data = feed.read()
		json_data = json.loads(text_data)
		synonyms = []
		for result in json_data['response']:
			if 'list' in result and 'synonyms' in result['list']:
				synonyms = synonyms + result['list']['synonyms'].split('|')
		return synonyms
	except urllib2.URLError, e:
		print "There was an error getting synyonyms for " + word + ": " + e

print getSynonyms("chair");