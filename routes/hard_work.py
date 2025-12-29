from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

class HardWorkRequestBody(BaseModel):
    url: str
    type: Literal['playlist', 'video', 'channel']

@router.post("/hard-work")
def fetch_transcript_and_embed():
    """
    fetches the transcript -> parses it -> generates(+stores) embeddings -> returns failed and passed urls, title, thumbnail
    """
    
    return None

