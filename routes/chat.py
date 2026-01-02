from fastapi import APIRouter, HTTPException, status
from lib.check_url_type import check_youtube_url_type
from metadata import fetch_metadata

router = APIRouter()

@router.post("/chat")
async def talk_to_llm(url: str):
    """
    initializes a chat with llm and works using websockets
    """
    # Check URL type first
    url_type = check_youtube_url_type(url)
    
    if url_type == 'invalid':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL provided"
        )
    
    # Fetch metadata based on the URL type
    metadata = await fetch_metadata(url_type=url_type, url=url)

    print('*'*50)
    print(metadata)
    print('*'*50)
    
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch metadata"
        )
    
    return None

