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