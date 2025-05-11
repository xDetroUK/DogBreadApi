from typing import List, Dict, Optional, Tuple
import re
import structlog

from src.models.breed import BreedLifespanResponse
from src.repositories.dog_api import fetch_breeds
from src.utils.pdf_export import generate_breeds_pdf

logger = structlog.get_logger()


def parse_lifespan(lifespan_str: str) -> Optional[Tuple[int, int]]:
    """
    Extract lifespan range (low, high) from string like '10 - 14 years'.
    Returns None if parsing fails.
    """
    if not lifespan_str:
        return None
    match = re.search(r"(\d+)\s*-\s*(\d+)", lifespan_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None


async def get_breeds_by_lifespan(min_years: int, max_years: int) -> List[BreedLifespanResponse]:
    try:
        breeds = await fetch_breeds()
        filtered = []

        for breed in breeds:
            lifespan_str = breed.get("life_span", "")
            parsed = parse_lifespan(lifespan_str)
            if parsed:
                low, high = parsed
                if low >= min_years and high <= max_years:
                    filtered.append(
                        BreedLifespanResponse(
                            name=breed.get("name", "Unknown"),
                            lifespan=lifespan_str,
                        )
                    )

        logger.info("Filtered breeds by lifespan", count=len(filtered))
        return filtered

    except Exception as e:
        logger.error("Failed to filter breeds by lifespan", error=str(e))
        return []


async def get_breeds_alphabetical() -> List[str]:
    try:
        breeds = await fetch_breeds()
        names = [breed.get("name", "").strip() for breed in breeds if "name" in breed]
        sorted_names = sorted(filter(None, names))
        logger.info("Retrieved alphabetical breed list", count=len(sorted_names))
        return sorted_names

    except Exception as e:
        logger.error("Failed to fetch alphabetical breeds", error=str(e))
        return []


async def export_breeds_pdf():
    try:
        breeds = await fetch_breeds()
        breeds_sorted = sorted(breeds, key=lambda b: b.get("name", ""))
        logger.info("Generating PDF with breeds", count=len(breeds_sorted))
        return generate_breeds_pdf(breeds_sorted)

    except Exception as e:
        logger.error("Failed to export breeds to PDF", error=str(e))
        return generate_breeds_pdf([])  # fallback to empty PDF
