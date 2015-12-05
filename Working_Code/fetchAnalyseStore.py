from apiclient.discovery import build
from apiclient.errors import HttpError
import unicodedata
import psycopg2
import re

playlist = {	'music':'PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI',
		'popular':'PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-',
		'news':'PL3ZQ5CpNulQldOL3T8g8k1mgWWysJfE9w',
		'sports':'PL8fVUTBmJhHJmpP7sLb9JfLtdwCmYX9xC' }


class apiYoutube:

	def __init__(self):

		DEVELOPER_KEY = "AIzaSyBLMlgZ-8BpNJX-jaDX0vPd4V9l7uisLaU"
		YOUTUBE_API_SERVICE_NAME = "youtube"
		YOUTUBE_API_VERSION = "v3"

		self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, \
			developerKey=DEVELOPER_KEY)


	def printData(self,category, infoList):
		videos = []
		count = 0
		print '================================================='
		print category
		print '================================================='
		for search_result in infoList.get("items", []):
			#videos.append("%s " % (search_result["snippet"]["title"]))
			print count, '\t', search_result['snippet']['resourceId']['videoId'], '\t', \
				unicodedata.normalize('NFKD', search_result['snippet']['title']).encode('ascii', 'ignore')
			count += 1
			self.getMeta(search_result['snippet']['resourceId']['videoId'])



	def getMeta(self, vid):

		video_response = self.youtube.videos().list(
			id=vid,
			part='statistics'
		).execute()

		for search_result in video_response.get("items", []):
			for key in search_result.get('statistics', []):
				print '\t\t', key,' :', search_result['statistics'][key]



	def writeToDB(self, category, playlist_response):
		conn = psycopg2.connect(database="mydb", user="postgres", password="harshit", host="127.0.0.1", port="5432")
		print "Opened database successfully"
		cur = conn.cursor()
		cur.execute("SELECT vID  from Video")
		rows = cur.fetchall()
		vIDs_from_DB = []
		for row in rows:
			vIDs_from_DB.append("%s" % (row[0]))
		try:
		
			for video in playlist_response.get("items", []):
				vID = unicodedata.normalize('NFKD', video['snippet']['resourceId']['videoId']).encode('ascii','ignore')
				list_containing_video_resource = self.youtube.videos().list(
					id=vID,
					part='snippet,statistics,contentDetails',
					fields='items(id, snippet/publishedAt, statistics/likeCount, statistics/dislikeCount, statistics/viewCount, statistics/commentCount, contentDetails/duration)'
				).execute()
				for video_resource in list_containing_video_resource.get("items", []):
					#Convert contentDetails/duration to bigint type i.e. no. of seconds 
					durationString = video_resource['contentDetails']['duration']
					durationSecs = 0
					if(durationString[0]=='P' and durationString[1]=='T'):
						matchObj = re.match( r'PT(\d+)?(M)?(\d+)?(S)?', durationString, re.M|re.I)
						if(matchObj.group(2)=='M' and matchObj.group(4)=='S'):
							#tempList = matchObj.groups('0')
							durationSecs = int(matchObj.group(1))*60 + int(matchObj.group(3))
						elif(matchObj.group(2)=='M'):
							durationSecs = int(matchObj.group(1))*60
						else:
							durationSecs = int(matchObj.group(1))
					#print durationSecs
					#print vIDs_from_DB
					# Now we have 'video' from playlist_response and its corresponding 'video_resource'
					# Now checking the existense of the fetched video in the 'Video' table
					# If found then write query to enter data in the DynamicData table only
					# Else write queries to make entries in both the tables
					if(vID not in vIDs_from_DB):
						if(vID=='Hvm3B6kXPK0'):
							print 'Stupid'
						cur.execute('''INSERT INTO Video (
									vID,
									title,
									duration,
									category,
									publishedAt)
								VALUES (%s,
									%s,
									%s,
									%s,
									%s)
							;''', (video['snippet']['resourceId']['videoId'],
								unicodedata.normalize('NFKD', video['snippet']['title']).encode('ascii', 'ignore'),
								durationSecs,
								category,
								video['snippet']['publishedAt'])
						)
					if('likeCount' not in video_resource['statistics']):
						video_resource['statistics']['likeCount'] = -1
					if('dislikeCount' not in video_resource['statistics']):
						video_resource['statistics']['dislikeCount'] = -1
					if('viewCount' not in video_resource['statistics']):
						video_resource['statistics']['viewCount'] = -1
					if('commentCount' not in video_resource['statistics']):
						video_resource['statistics']['commentCount'] = -1
					if(vID=='Hvm3B6kXPK0'):
						print 'Harshit',video_resource['statistics']['likeCount'], video_resource['statistics']['dislikeCount'], video_resource['statistics']['viewCount'], video_resource['statistics']['commentCount']
					cur.execute('''INSERT INTO DynamicData (
								extractionTime, 
								videoID, 
								likeCount, 
								dislikeCount, 
								viewCount, 
								commentCount, 
								rank, 
								posSent, 
								neuSent, 
								negSent)
							VALUES (LOCALTIMESTAMP,
								%s,
								%s,
								%s,
								%s,
								%s,
								%s,
								0,
								0,
								0)
						;''', (vID,
							video_resource['statistics']['likeCount'],
							video_resource['statistics']['dislikeCount'],
							video_resource['statistics']['viewCount'],
							video_resource['statistics']['commentCount'],
							video['snippet']['position']))
		except:
			print 	vID, video_resource['contentDetails']['duration'], durationSecs
			return
		conn.commit()
		#conn.close()



	def getVideos(self, category, pid):

		next_page_token = ''

		flag = True
		count = 0

		while count < 2 and flag == True:
			playlist_response = self.youtube.playlistItems().list(
				playlistId=pid,
				part='id,snippet',
				maxResults=50,
				pageToken=next_page_token
			).execute()
			count += 1

			if 'nextPageToken' in playlist_response:
				next_page_token = playlist_response['nextPageToken']
			else:
				flag = False

			#self.printData(category, playlist_response)
			print 'LOOP CALLED'
			self.writeToDB(category, playlist_response)

	

if __name__ == "__main__":

	#global playlist
	api = apiYoutube()
	for key in playlist:
		 api.getVideos(key,playlist[key])

