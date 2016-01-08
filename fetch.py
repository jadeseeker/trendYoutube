from apiclient.discovery import build
from apiclient.errors import HttpError
import unicodedata


playlist = {'music':'PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI',
			'popular':'PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-',
			'news':'PL3ZQ5CpNulQldOL3T8g8k1mgWWysJfE9w',
			'sports':'PL8fVUTBmJhHJmpP7sLb9JfLtdwCmYX9xC' }


class apiYoutube:

	def __init__(self):

		DEVELOPER_KEY = #"<google api key>"
		YOUTUBE_API_SERVICE_NAME = "youtube"
		YOUTUBE_API_VERSION = "v3"

		self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, \
			developerKey=DEVELOPER_KEY)


	def subComments(self, cid):

		results = self.youtube.comments().list(
					part = "snippet",
					parentId = cid,
					textFormat = "plainText",
					maxResults = 100,
					fields = 'items(snippet/textDisplay)'
				  ).execute()
				
		for item in results["items"]:
			text = item["snippet"]["textDisplay"]
			#print '\t\t\t\t', text[:10]
		


	def getComments(self,vid):

		count = 0
		flag = True
		next_page_token = ''
		try:

			while flag == True: #count < 1 and flag == True:
				results = self.youtube.commentThreads().list(
						part = "snippet",
						videoId = vid,
						maxResults = 100,
						textFormat = "plainText",
						pageToken = next_page_token,
						fields = 'items(id, snippet/totalReplyCount, snippet/topLevelComment/snippet/textDisplay)'
					).execute()
				count+=1

				if 'nextPageToken' in results:
					next_page_token = results['nextPageToken']
				else:
					flag = False

			
			for item in results["items"]:
				comment = item["snippet"]["topLevelComment"]
				cid = item['id']
								
				text = unicodedata.normalize('NFKD', comment["snippet"]["textDisplay"]
					).encode('ascii', 'ignore') 
				
				replyCount = item["snippet"]["totalReplyCount"]

				#print '\t\t\t', cid

				if replyCount > 0:
					self.subComments(cid)

		except:
			print 'COMMENTS NOT AVAILABLE'


	def getMeta(self, vid):

		video_response = self.youtube.videos().list(
			id = vid,
			part = 'statistics'
		).execute()

		
		for search_result in video_response['items']:
			for key in search_result['statistics']:
				print '\t\t', key,' :', search_result['statistics'][key]
				#pass
		

		self.getComments(vid)


	def printData(self,category, infoList):
		videos = []
		count = 0
		print '================================================='
		print category
		print '================================================='
		for search_result in infoList['items']:
			vid = search_result['snippet']['resourceId']['videoId']
			title = unicodedata.normalize('NFKD', 
				search_result['snippet']['title']).encode('ascii', 'ignore') 
			
			print count, '\t', vid, '\t', title
			count += 1
			
			self.getMeta(vid)


	def getVideos(self, category, pid):

		next_page_token = ''

		flag = True
		count = 0

		while count < 2 and flag == True:
			playlist_response = self.youtube.playlistItems().list(
				playlistId = pid,
				part = 'id,snippet',
				maxResults = 50,
				pageToken = next_page_token
			).execute()
			count += 1

			if 'nextPageToken' in playlist_response:
				next_page_token = playlist_response['nextPageToken']
			else:
				flag = False

			self.printData(category, playlist_response)

		

	

if __name__ == "__main__":

	#global playlist
	api = apiYoutube()
	#api.getMeta('mQPjKSVe1tQ')
	for key in playlist:
		api.getVideos(key,playlist[key])

