from textblob import TextBlob

# to be able to run this code, go to your python folder
# and type the following two commands:
#
# pip install -U textblob
# python -m textblob.download_corpora

def sentiment(message):
	text = TextBlob(message)
	response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity }
	return response

entry = raw_input("Enter text: ")

response = sentiment(entry)

print response
if response['polarity'] < -0.33:
	print 'negative'
elif response['polarity'] < 0.33:
	print 'neutral'
else: print 'positive'