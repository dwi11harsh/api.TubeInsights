from typing import Optional, Dict, Any
from playwright.async_api import Page, BrowserContext


async def setup_page_with_cookies(page: Page, context: BrowserContext, crawler_state: Optional[Dict[str, Any]] = None) -> None:
    async def block_resource(route):
        await route.abort()
    
    await page.route('**/*.webp', block_resource)
    await page.route('**/*.jpg', block_resource)
    await page.route('**/*.jpeg', block_resource)
    await page.route('**/*.png', block_resource)
    await page.route('**/*.svg', block_resource)
    await page.route('**/*.gif', block_resource)
    await page.route('**/*.woff', block_resource)
    await page.route('**/*.pdf', block_resource)
    await page.route('**/*.zip', block_resource)
    
    if crawler_state and 'cookies' in crawler_state and context:
        cookies = crawler_state['cookies']
        if cookies:
            await context.add_cookies(cookies)


def request_domain_transform(request_url: str) -> str:
    if 'consent.youtube' in request_url:
        return request_url.replace('consent.youtube', 'www.youtube')
    return request_url

