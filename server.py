from flask import Flask
from flask import render_template
from twython import Twython

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
	results = twitter.search(q='$'+query, count=100)

	tweetText = [tweet['text'] for tweet in results['statuses']]
	resultsLength = len(results['statuses'])
	lastID = results['statuses'][-1]['id_str']

	while resultsLength == 100 and len(tweetText) < 1998:
		results = twitter.search(q=query, count=100, max_id=lastID)
		

