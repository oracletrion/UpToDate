from django.shortcuts import get_object_or_404, render

from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import argparse
import requests
import logging
import googleapiclient.discovery
'''
DEVELOPER_KEY = 'AIzaSyBb8g3wV9IIkwvtgYb1HhGPsS1kVA7gWEM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(
    q=options.q,
    type='video',
    location=options.location,
    locationRadius=options.location_radius,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  search_videos = []

  for search_result in search_response.get('items', []):
    search_videos.append(search_result['id']['videoId'])
  video_ids = ','.join(search_videos)

  # Call the videos.list method to retrieve location details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, recordingDetails'
  ).execute()

  videos = []

  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get('items', []):
    videos.append('%s, (%s,%s)' % (video_result['snippet']['title'],
                              video_result['recordingDetails']['location']['latitude'],
                              video_result['recordingDetails']['location']['longitude']))

  print 'Videos:\n', '\n'.join(videos), '\n'

'''
def index(request):
    return HttpResponse("This is the youtube index.")

def form(request):
    return render(request, 'youtube/index.html')
