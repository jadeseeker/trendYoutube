#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBLMlgZ-8BpNJX-jaDX0vPd4V9l7uisLaU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

video_response = youtube.videos().list(
  id='RFDatCchpus',
  part='statistics'
).execute()

#print video_response

#metaData = []


for search_result in video_response.get("items", []):
  #print search_result
  for key in search_result.get('statistics', []):
    print key,' :', search_result['statistics'][key]

#videos.append("%s " % (search_result["snippet"]["title"]))
