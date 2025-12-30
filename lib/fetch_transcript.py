from lib.check_url_type import URLType
from transcript.channel import fetch_channel_transcript
from transcript.playlist import fetch_playlist_transcripts
from transcript.video import fetch_video_transcript

async def check_type_and_fetch_transcript(url:str, type: URLType):
    if type == 'channel':
        fetch_channel_transcript(url)
    elif type == 'playlist':
        fetch_playlist_transcripts(url)
    elif type == 'mixed' or type == 'video':
        fetch_video_transcript(url)
    else:
        return None