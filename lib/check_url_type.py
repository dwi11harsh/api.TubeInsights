"""Module for checking and validating YouTube URL types."""

from typing import Literal
from urllib.parse import urlparse, parse_qs

URLType = Literal['playlist', 'video', 'channel', 'mixed', 'invalid']


def check_youtube_url_type(url: str) -> URLType:
    """Check and identify the type of a YouTube URL.
    
    Args:
        url: The URL string to check (will be prefixed with 'https://' if needed).
    
    Returns:
        URLType: One of 'playlist', 'video', 'channel', 'mixed', or 'invalid'.
    """
    if not isinstance(url, str) or not (url := url.lower().strip()):
        return 'invalid'

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urlparse(url)
        host_name = parsed.hostname
        is_youtube = host_name and ('youtube.com' in host_name or 'youtu.be' in host_name)

        if not is_youtube:
            raise Exception('Not a youtube url')

        path = parsed.path
        has_channel = '/channel/' in path or '/c/' in path or '/user/' in path or path.startswith('/@')
        if has_channel:
            return 'channel'

        params = parse_qs(parsed.query)
        path = parsed.path

        has_video= '/watch' in path and 'v' in params
        
        has_playlist = '/playlist' in path or 'list' in params

        if has_video and has_playlist:
            return 'mixed'

        if has_playlist:
            return 'playlist'

        if has_video:
            return 'video'

        return 'invalid'
        
    except Exception as e:
        return 'invalid'