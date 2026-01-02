import asyncio
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Optional
from playwright.async_api import Page, Route, Request


async def extract_transcript_url(page: Page, timeout: float = 20.0) -> Optional[str]:
    transcript_future: asyncio.Future[str] = asyncio.Future()
    
    async def handle_transcript_request(route: Route, request: Request) -> None:
        if not transcript_future.done():
            transcript_future.set_result(request.url)
        await route.fulfill(status=200)
    
    try:
        await page.route('**/api/timedtext**', handle_transcript_request)
        
        try:
            await page.wait_for_selector('.ytp-subtitles-button', state='visible', timeout=10000)
        except Exception:
            return None
        
        await page.click('.ytp-subtitles-button')
        transcript_url = await asyncio.wait_for(transcript_future, timeout=timeout)
        
        parsed_url = urlparse(transcript_url)
        query_params = parse_qs(parsed_url.query)
        query_params.pop('fmt', None)
        new_query = urlencode(query_params, doseq=True)
        cleaned_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
        
        return cleaned_url
    except asyncio.TimeoutError:
        return None
    except Exception as e:
        print(f'error occurred while extracting transcript url: {e}')
        return None
    finally:
        try:
            await page.unroute('**/api/timedtext**', handle_transcript_request)
        except Exception:
            pass

