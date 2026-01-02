from typing import Optional, Dict, Any
from playwright.async_api import Page, BrowserContext


async def extract_video_data_from_page(page: Page, url: str, context: Optional[BrowserContext] = None, crawler_state: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    try:
        await page.locator('h1').first.wait_for(state='attached')
        
        try:
            cookies_button = page.locator('button[aria-label*="Accept"]').first
            if await cookies_button.is_visible(timeout=3000):
                await cookies_button.click()
                if context and crawler_state is not None:
                    cookies_state = [cookie for cookie in await context.cookies() if cookie['name'] == 'SOCS']
                    if cookies_state:
                        if 'cookies' not in crawler_state:
                            crawler_state['cookies'] = []
                        crawler_state['cookies'] = cookies_state
        except Exception:
            pass
        
        await page.wait_for_function('window.ytInitialPlayerResponse !== undefined', timeout=15000)
        
        video_data = await page.evaluate('window.ytInitialPlayerResponse')
        
        if not video_data:
            return None
        
        video_details = video_data.get('videoDetails', {})
        microformat = video_data.get('microformat', {}).get('playerMicroformatRenderer', {})
        
        main_data = {
            'url': url,
            'title': video_details.get('title'),
            'description': video_details.get('shortDescription'),
            'channel': video_details.get('author'),
            'channel_id': video_details.get('channelId'),
            'video_id': video_details.get('videoId'),
            'duration': video_details.get('lengthSeconds'),
            'keywords': video_details.get('keywords'),
            'view_count': video_details.get('viewCount'),
            'like_count': microformat.get('likeCount'),
            'is_shorts': microformat.get('isShortsEligible'),
            'publish_date': microformat.get('publishDate'),
        }
        
        return main_data
    except Exception as e:
        print(f'error occurred while extracting video data from url[{url}]: {e}')
        return None

