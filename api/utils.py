from dateutil import parser
from datetime import datetime, timedelta

from api.models import APIKey
from api.constants import YT_API_URL

import requests


def get_youtube_videos(search_query, max_results):
    """
    Retrieve list of YouTube videos matching the search query.
    """
    # Get list of all API keys which haven't expired yet.
    api_keys = APIKey.objects.filter(has_expired=False)
    if len(api_keys) < 1:
        return {"message": "FAILURE", "result": "No valid API Keys found!"}

    # Try to fetch results from YT using all API keys which haven't expired yet.
    # Update `has_expired` field of APIKey Object if expired.
    # If API key works, break
    for key in api_keys:
        # Retrieve videos dated upto 1 month back
        published_after = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
        query_params = {
            "key": key.api_key,
            "q": search_query,
            "maxResults": max_results,
            "publishedAfter": published_after,
            "part": "snippet",
            "order": "date"
        }

        try:
            res = requests.get(YT_API_URL, query_params)
        except Exception as e:
            return {"message": "FAILURE", "result": "Failed to get results from YT."}

        if res.status_code == 200:
            return {"message": "SUCCESS", "result": res.json()}
        elif res.status_code == 403:
            key.has_expired = True
            key.save()
        else:
            return {"message": "FAILURE", "result": "Failed to get results from YT."}

    return {"message": "FAILURE", "result": "Failed to get results from YT."}


def parse_youtube_search_response(response):
    """
    Parse required data from YouTube's search API response.
    """
    videos = []
    for item in response['items']:
        video_data = dict()
        if item['id']['kind'] == 'youtube#video':
            video_data['youtube_video_id'] = item['id']['videoId']
            video_data['published_at'] = parser.parse(item['snippet']['publishedAt'])
            video_data['title'] = item['snippet']['title']
            video_data['description'] = item['snippet']['description']
            video_data['thumbnail_url'] = item['snippet']['thumbnails']['default']['url']

        videos.append(video_data)

    return videos
