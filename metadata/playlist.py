from typing import Union, Optional, Dict, Any, List
from pydantic import BaseModel
from playwright.async_api import async_playwright

from metadata.lib.extract_video_urls import extract_video_urls_from_page
from metadata.lib.setup_page import setup_page_with_cookies
from metadata.video import fetch_video_metadata


class PlaylistMetadata(BaseModel):
    url: str
    video_count: int
    video_urls: List[str]
    videos: Optional[List[Dict[str, Any]]] = None


async def fetch_playlist_metadata(url: str, include_video_metadata: bool = False, limit: Optional[int] = None, crawler_state: Optional[Dict[str, Any]] = None) -> Union[PlaylistMetadata, None]:
    playwright = None
    browser = None
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await setup_page_with_cookies(page, context, crawler_state)
        
        await page.goto(url, wait_until='networkidle')
        
        video_urls = await extract_video_urls_from_page(page, limit)
        
        await browser.close()
        await playwright.stop()
        
        if not video_urls:
            return None
        
        videos_metadata = None
        if include_video_metadata:
            videos_metadata = []
            for video_url in video_urls:
                video_meta = await fetch_video_metadata(video_url, include_transcript=False, crawler_state=crawler_state)
                if video_meta:
                    videos_metadata.append({
                        'url': video_meta.url,
                        'id': video_meta.id,
                        'name': video_meta.name,
                        'channel': video_meta.channel,
                        'length': video_meta.lenght,
                    })
        
        return PlaylistMetadata(
            url=url,
            video_count=len(video_urls),
            video_urls=video_urls,
            videos=videos_metadata
        )
    except Exception as e:
        print(f'error occurred while fetching playlist metadata from url[{url}]: {e}')
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        return None

