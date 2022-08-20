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