import os
import googleapiclient.discovery
import googleapiclient.errors
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from urllib.parse import parse_qs

load_dotenv()
api_key = "AIzaSyDC4Z0NFdTTN6_FKeFxpcRlGnaLFBhL0lQ"

def get_comments(youtube, **kwargs):
    comments = []
    results = youtube.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # check if there are more comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments

def main(video_id, api_key):
    # Disable OAuthlib's HTTPs verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key)

    comments = get_comments(youtube, part="snippet", videoId=video_id, textFormat="plainText")
    return comments


def get_video_comments(video_id):
    return main(video_id, api_key)


def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """

    query = urlparse(value)
    p = parse_qs(query.query)
    print(p['v'][0])
    video_id = p['v'][0]
    video_id = video_id.split('-')
    if len(video_id) > 1:
        if len(video_id[0]) > len(video_id[1]):
            return video_id[0]
        else:
            return video_id[1]
    else:
        return video_id[0]

    
    # fail?

video_url = "https://www.youtube.com/watch?v=qW7CGTK-1vA&ab_channel=LastWeekTonight"
video_url2 = "https://www.youtube.com/watch?v=pZ-MpxDZr9I&ab_channel=BeastPhilanthropy"
video_url3 = "https://www.youtube.com/watch?v=laGVW1E09dU&t=997s&ab_channel=IWDominate"
print(video_id(video_url))
print(video_id(video_url2))
print(video_id(video_url3))

