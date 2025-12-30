from typing import Union, Optional, Any
from pydantic import BaseModel
from pytube import YouTube


class VideoMetadata(BaseModel):
    url: str
    id: str
    name: str
    channel: str
    lenght: Union[str, None]


def safe_get_attr(obj: Any, attr_name: str, default: Optional[Any] = None) -> Optional[Any]:
    try:
        return getattr(obj, attr_name)
    except Exception:
        return default


async def fetch_video_metadata(url:str)-> Union[VideoMetadata, None]:
    try:
        yt = YouTube(url)
        
        vars_dict = {
            'title': safe_get_attr(yt, 'title'),
            'thumbnail': safe_get_attr(yt, 'thumbnail_url'),
            'description': safe_get_attr(yt, 'description'),
            'length': safe_get_attr(yt, 'length'),
            'author': safe_get_attr(yt, 'author'),
            'channel_id': safe_get_attr(yt, 'channel_id'),
            'channel_url': safe_get_attr(yt, 'channel_url'),
            'publish_date': safe_get_attr(yt, 'publish_date'),
        }
        
        non_none_vars = [name for name, value in vars_dict.items() if value is not None]
        print('Variables that are not None:', non_none_vars)
        
        none_vars = [name for name, value in vars_dict.items() if value is None]
        if none_vars:
            print('Variables that are None (failed to retrieve):', none_vars)
        
        return None
    except Exception as e:
        print('exception occurred', str(e))
        return None