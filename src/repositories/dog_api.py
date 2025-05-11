import logging
import json
import asyncio
from typing import List, Dict

from httpx import AsyncClient, HTTPStatusError, RequestError
import redis.asyncio as redis

from src.config.settings import settings

logger = logging.getLogger(__name__)

REDIS_KEY = "dog_api:breeds"
REDIS_TTL_SECONDS = 60 * 10  # 10 minutes


async def fetch_breeds() -> List[Dict]:
    """
    Fetch breed data from the Dog API with retry logic and Redis caching.
    Returns empty list on failure.
    """
    try:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

        # Try cache first
        cached = await redis_client.get(REDIS_KEY)
        if cached:
            logger.info("Loaded breeds from Redis cache")
            return json.loads(cached)

        url = f"{settings.dog_api_url}/breeds"

        for attempt in range(3):
            try:
                async with AsyncClient(timeout=10) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    data = response.json()

                    if not isinstance(data, list):
                        logger.error(f"Expected list, got: {type(data)} - content: {data}")
                        return []

                    await redis_client.set(REDIS_KEY, json.dumps(data), ex=REDIS_TTL_SECONDS)
                    logger.info(f"Fetched {len(data)} breeds from Dog API (attempt {attempt + 1})")
                    return data

            except (HTTPStatusError, RequestError) as err:
                logger.warning(f"Attempt {attempt + 1} failed: {err}")
                await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Unexpected error in fetch_breeds: {e}")

    return []
