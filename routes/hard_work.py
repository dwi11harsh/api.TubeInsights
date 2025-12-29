from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

class HardWorkRequestBody(BaseModel):
    url: str
    type: Literal['playlist', 'video', 'channel']

@router.post("/hard-work")
def fetch_transcript_and_embed(body: HardWorkRequestBody):
    # destructure request-body
    url = body.url
    type = body.type

    # do another type check in case the url is not of the mentioned type
    

