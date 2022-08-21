from celery import shared_task

from api.utils import get_youtube_videos, parse_youtube_search_response
from api.models import Video


@shared_task()
def store_video_data():
    """
    Retrieve YT video data `get_youtube_videos` function and store
    video data in db.
    """
    youtube_videos = get_youtube_videos(search_query='programming', max_results=5)
    if youtube_videos['message'] == 'SUCCESS':
        videos = parse_youtube_search_response(youtube_videos['result'])
        for video in videos:
            # Check if video with same id exists.
            try:
                existing_video = Video.objects.get(youtube_video_id=video['youtube_video_id'])
            except Video.DoesNotExist:
                video_obj = Video(**video)
                video_obj.save()
    else:
        # TODO: Add logger
        print(youtube_videos['result'])