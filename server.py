#from nltk.classify import NaiveBayesClassifier
#from nltk.corpus import subjectivity
#from nltk.sentiment import SentimentAnalyzer
#from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from nltk import tokenize
#from nltk.twitter import Twitter
from flask import Flask
from flask import render_template
from twython import Twython
import json
app = Flask(__name__)


CONSUMER_KEY='xmNzm2YKn1LyBBQA32YzQpLix'
CONSUMER_SECRET='7d4vGazTVoVOSLmH2zWMVWGIXotlAyFeqkWMHLJWdG3othjv6B'
ACCESS_KEY='375094867-N1P09cdmtPB43vMsYmMa77LgD5u1bSASdCYBLvqN'
ACCESS_SECRET='vV20CFJUodqdrGMW1vLZhHzzQkAvRV8upV5TSx7BrSn8x'

@app.route('/')
def hello_world():
	return render_template('index.html.j2', title="Tweet Stock Ticker")

@app.route('/query/<string:query>')
def query(query):
	twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
	tweets = searchTwitter(twitter, query)
	values, percPos, percNeg = analyzeTweets(tweets)
	return json.dumps({
		"data": list(filter(lambda t: t[1] != 0, zip(tweets, values))),
		"percentPositive": percPos,
		"percentNegative": percNeg
	}, indent=0)	
	

def searchTwitter(twitter, query, length=2000):
	tweetText = []
	resultsLength = 100
	lastID = None

	while resultsLength == 100 and len(tweetText) < length - 2:
		results = twitter.search(q='$'+query, count=100, max_id=lastID)
		tweetText.extend([tweet['text'] for tweet in results['statuses']])
		resultsLength = len(results['statuses'])
		lastID = results['statuses'][-1]['id_str']

	return tweetText

def tweetsToSentiments(sentences, sid=SentimentIntensityAnalyzer()):
	return [sid.polarity_scores(sentence)["compound"] for sentence in sentences]

def analyzeTweets(tweets):
	values = tweetsToSentiments(tweets)
	positiveCount = 0
	negativeCount = 0

	for value in values:
		if value > 0:
			positiveCount += 1
		elif value < 0:
			negativeCount += 1

	percentPositive = (positiveCount * 100) / len(values)
	percentNegative = (negativeCount * 100) / len(values)

	return (values, percentPositive, percentNegative)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)