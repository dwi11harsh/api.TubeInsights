from typing import Union, Optional, Dict, Any
from pydantic import BaseModel
from playwright.async_api import async_playwright

from metadata.lib.extract_video_data import extract_video_data_from_page
from metadata.lib.extract_transcript_url import extract_transcript_url
from metadata.lib.extract_transcript import extract_transcript_from_response, enrich_video_data_with_transcript
from metadata.lib.setup_page import setup_page_with_cookies


class VideoMetadata(BaseModel):
    url: str
    id: str
    name: str
    channel: str
    lenght: Union[str, None]


async def fetch_video_metadata(url: str, include_transcript: bool = False, crawler_state: Optional[Dict[str, Any]] = None) -> Union[VideoMetadata, None]:
    playwright = None
    browser = None
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await setup_page_with_cookies(page, context, crawler_state)
        
        await page.goto(url, wait_until='networkidle')
        
        video_data = await extract_video_data_from_page(page, url, context, crawler_state)
        
        if not video_data:
            return None
        
        if include_transcript:
            transcript_url = await extract_transcript_url(page)
            if transcript_url:
                response = await page.goto(transcript_url, wait_until='networkidle')
                if response:
                    transcript = await extract_transcript_from_response(response)
                    if transcript:
                        video_data = enrich_video_data_with_transcript(video_data, transcript)
        
        await browser.close()
        await playwright.stop()
        
        return VideoMetadata(
            url=video_data.get('url', url),
            id=video_data.get('video_id', ''),
            name=video_data.get('title', ''),
            channel=video_data.get('channel', ''),
            lenght=str(video_data.get('duration', '')) if video_data.get('duration') else None
        )
    except Exception as e:
        print(f'error occurred while fetching video metadata from url[{url}]: {e}')
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        return None