from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Literal

from metadata import video
from transcript.channel import fetch_channel_transcript
from transcript.playlist import fetch_playlist_transcripts
from transcript.video import fetch_video_transcript
from lib.check_url_type import URLType, check_youtube_url_type

router = APIRouter()

class HardWorkRequestBody(BaseModel):
    url: str
    type: Literal['playlist', 'video', 'channel']

class HardWorkResponseBody(BaseModel):
    type: URLType


FETCH_FUNCTIONS = {
    'video': fetch_video_transcript,
    'playlist': fetch_playlist_transcripts,
    'channel': fetch_channel_transcript,
}

@router.post("/hard-work", status_code=status.HTTP_202_ACCEPTED)
async def fetch_transcript_and_embed(body: HardWorkRequestBody):
    url = body.url

    # do another type check in case the url is not of the mentioned type
    type = check_youtube_url_type(url)

    if type == 'invalid':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL provided"
        )

    # TODO: later add a way to ask user for 'video'/'playlist' transcript fetch in case of 'mixed' type

    await video.fetch_video_metadata(url)

    return None
    
    

