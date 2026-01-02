from typing import List, Optional
from playwright.async_api import Page
from bs4 import BeautifulSoup


async def extract_video_urls_from_page(page: Page, limit: Optional[int] = None) -> List[str]:
    try:
        await page.locator('h1').first.wait_for(state='attached')
        
        try:
            cookies_button = page.locator('button[aria-label*="Accept"]').first
            if await cookies_button.is_visible(timeout=3000):
                await cookies_button.click()
        except Exception:
            pass
        
        await page.locator('a[href*="watch"]').first.wait_for()
        
        previous_height = 0
        current_height = await page.evaluate('document.body.scrollHeight')
        scroll_attempts = 0
        max_scroll_attempts = 50
        
        while current_height != previous_height and scroll_attempts < max_scroll_attempts:
            previous_height = current_height
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await page.wait_for_timeout(3000)
            await page.wait_for_load_state('networkidle', timeout=5000)
            current_height = await page.evaluate('document.body.scrollHeight')
            scroll_attempts += 1
            
            if limit:
                video_urls = await _extract_urls_from_page_content(page)
                if len(video_urls) >= limit:
                    return video_urls[:limit]
        
        video_urls = await _extract_urls_from_page_content(page)
        
        if limit:
            return video_urls[:limit]
        
        return video_urls
    except Exception as e:
        print(f'error occurred while extracting video urls: {e}')
        return []


async def _extract_urls_from_page_content(page: Page) -> List[str]:
    page_html = await page.content()
    soup = BeautifulSoup(page_html, 'html.parser')
    
    video_urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/watch?v=' in href:
            full_url = f"https://www.youtube.com{href}" if href.startswith('/') else href
            if full_url not in video_urls:
                video_urls.append(full_url)
    
    return video_urls

