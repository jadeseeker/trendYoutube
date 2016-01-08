#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = #"google api key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  next_page_token = ''
  #while next_page_token is not None:
  playlistitems_response = youtube.playlistItems().list(
      playlistId="PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI",
      part='id,snippet',
      maxResults=50,
      pageToken=next_page_token
  ).execute()

  #print playlistitems_response
  '''
  search_response = youtube.playlistItems().list(
    playlistID=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()
  '''
  videos = []
  #channels = []
  #playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in playlistitems_response.get("items", []):
    #print search_result
    #if search_result['id']['kind'] == "youtube#video":
    videos.append("%s " % (search_result["snippet"]["title"]))
                                #search_result["id"]["videoId"]))
    '''
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
    '''

  print "Videos:\n", "\n".join(videos), "\n"
  #print "Channels:\n", "\n".join(channels), "\n"
  #print "Playlists:\n", "\n".join(playlists), "\n"
  


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
