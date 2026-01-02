import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from playwright.async_api import Response


async def extract_transcript_from_response(response: Response) -> Optional[str]:
    try:
        response_text = await response.text()
        root = ET.fromstring(response_text)
        transcript_data = [text_element.text.strip() for text_element in root.findall('.//text') if text_element.text]
        transcript = '\n'.join(transcript_data)
        return transcript
    except ET.ParseError:
        print('incorrect xml response')
        return None
    except Exception as e:
        print(f'error occurred while extracting transcript: {e}')
        return None


async def enrich_video_data_with_transcript(video_data: Dict[str, Any], transcript: str) -> Dict[str, Any]:
    video_data['transcript'] = transcript
    return video_data

