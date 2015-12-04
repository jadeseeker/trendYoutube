import pandas as pd
from sklearn import svm

#variables
file = 'dynamicdata.txt'
category = 'popular'
min_days_ranked = 3
days_trained = 12
gam = 0.001
c = 100.

# Read in data and set up initial tables
data = pd.read_csv(file, sep="\t", skiprows=[0], header=None)
data.columns = ['Date/Time', 'VID', 'Likes', 'Dislikes', 'Views',
				'Comments', 'Rank', 'Positive', 'Neutral', 'Negative']
vidinfo = pd.read_csv('video.txt', sep="\t", skiprows=[0], header=None)
vidinfo.columns = ['VID', 'Title', 'Duation', 'Category', 'Published']

# Create empty tables to hold delta data and test data
training = pd.DataFrame()
#testdata = pd.DataFrame()

# Separate data by video ID and sort data by timestamp
videos = vidinfo[vidinfo.Category == category].VID.unique()
for vid in videos:
	vdata = (data[data.VID == vid]).sort_values(by='Date/Time')
	
	# Ignore video dataset for training if min days of data not met
	if len(vdata.index) >= min_days_ranked:
		## for averaged delta feed
		# Index data by VID and timestamp and generate deltas
		vdeltas = vdata.set_index(['VID', 'Date/Time']).diff()		
		
		##for later testing
		#if len(vdeltas.index) >= days_trained + 1:
		#	testdata = testdata.append(vdeltas[-3:], ignore_index = True)
		
		# Condense list of deltas into averages
		# Only use the first X days, as specified for training
		vdeltas_means = vdeltas[1:days_trained].mean(level=0)
		# Append data to the training information table
		training = training.append(vdeltas_means, ignore_index=True)
		
		## For raw data feed
		#training = training.append(vdata[vdata.columns[2:]], ignore_index=True)

# Move Rank to front of arrays, for better arrangement
training = training[['Rank', 'Likes', 'Dislikes', 'Views',
				'Comments', 'Positive', 'Neutral', 'Negative']]
#testdata = testdata[['Rank', 'Likes', 'Dislikes', 'Views',
#				'Comments', 'Positive', 'Neutral', 'Negative']]

# Preview of condensed data
print training[:10]
#print testdata[:10]

# Write to external file
#training.to_csv('deltas.csv',index=False)

# Remove rank from training data and generate "goal" targets
tdata = training[training.columns[1:]]
target = pd.DataFrame(columns=['Goal'])
# Negative rank delta means increase in rank (1), positive => decrease
for x in range(0, len(training.index)):
	if training['Rank'][x] < 0:
		target.loc[x] = 1
	elif training['Rank'][x] > 0:
		target.loc[x] = -1
	else: target.loc[x] = 0

# Generating classifier
clf = svm.SVC(gamma=gam, C=c)
clf.fit(tdata, target.ix[:,0])

# Single test sample
print tdata[-1:]
print target[-1:]

print clf.predict(tdata[-1:])