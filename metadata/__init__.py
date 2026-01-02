from typing import Union, Optional, Dict, Any
from lib.check_url_type import URLType

from metadata.channel import fetch_channel_metadata, ChannelMetadata
from metadata.playlist import fetch_playlist_metadata, PlaylistMetadata
from metadata.video import fetch_video_metadata, VideoMetadata


async def fetch_metadata(
    url_type: URLType,
    url: str,
    include_video_metadata: bool = False,
    include_transcript: bool = True,
    limit: Optional[int] = None,
    crawler_state: Optional[Dict[str, Any]] = None
) -> Union[ChannelMetadata, PlaylistMetadata, VideoMetadata, None]:
    """Fetch metadata based on URL type.
    
    Args:
        url_type: The type of URL ('playlist', 'video', 'channel', 'mixed', or 'invalid')
        url: The YouTube URL to fetch metadata for
        include_video_metadata: For channel/playlist, whether to include full video metadata
        include_transcript: For video, whether to include transcript
        limit: Optional limit for number of videos to fetch (for channel/playlist)
        crawler_state: Optional crawler state for maintaining session
    
    Returns:
        ChannelMetadata, PlaylistMetadata, VideoMetadata, or None if invalid/error
    """
    if url_type == 'channel':
        return await fetch_channel_metadata(
            url,
            include_video_metadata=include_video_metadata,
            limit=limit,
            crawler_state=crawler_state
        )
    elif url_type == 'playlist':
        return await fetch_playlist_metadata(
            url,
            include_video_metadata=include_video_metadata,
            limit=limit,
            crawler_state=crawler_state
        )
    elif url_type == 'video':
        return await fetch_video_metadata(
            url,
            include_transcript=include_transcript,
            crawler_state=crawler_state
        )
    elif url_type == 'mixed':
        # For mixed URLs (video with playlist), fetch video metadata
        return await fetch_video_metadata(
            url,
            include_transcript=include_transcript,
            crawler_state=crawler_state
        )
    else:  # 'invalid'
        return None

