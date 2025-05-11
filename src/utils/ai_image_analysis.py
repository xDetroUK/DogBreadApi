from typing import Optional
from openai import OpenAI
from src.config.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


async def analyze_image_url(image_url: str) -> Optional[str]:
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "What breed or details can you describe from this image?"},
                    {"type": "input_image", "image_url": image_url},
                ],
            }],
        )
        return response.output_text.strip()
    except Exception as e:
        return f"OpenAI API error: {str(e)}"
