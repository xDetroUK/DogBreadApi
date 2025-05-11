from fastapi import APIRouter, Query, HTTPException, status, Form
from typing import List
from src.services.breed_service import (
    get_breeds_by_lifespan,
    get_breeds_alphabetical,
    export_breeds_pdf,
)
from pydantic import BaseModel
from src.models.breed import BreedLifespanResponse
from fastapi.responses import StreamingResponse
import structlog
from src.utils.ai_image_analysis import analyze_image_url
from typing import Optional
from src.utils.match_breed import match_best_breed

logger = structlog.get_logger()

router = APIRouter(prefix="/breeds", tags=["breeds"])

class BreedMatchRequest(BaseModel):
    preferences: str


@router.get("/lifespan", response_model=List[BreedLifespanResponse])
async def breeds_by_lifespan(
    min_years: int = Query(..., ge=0),
    max_years: int = Query(..., ge=0)
):
    """
    Get dog breeds with lifespan between min_years and max_years.
    """
    if min_years > max_years:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_years must be less than or equal to max_years",
        )

    try:
        breeds = await get_breeds_by_lifespan(min_years, max_years)
        if not breeds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No breeds found in the specified lifespan range",
            )
        return breeds
    except Exception as e:
        logger.error("Error fetching lifespan breeds", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching breeds by lifespan",
        )


@router.get("/alphabetical", response_model=List[str])
async def alphabetical_breeds():
    """
    Get all dog breeds sorted alphabetically.
    """
    try:
        breeds = await get_breeds_alphabetical()
        if not breeds:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No breeds found from the Dog API",
            )
        return breeds
    except Exception as e:
        logger.error("Error fetching alphabetical breeds", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching alphabetical breeds",
        )


@router.get("/export/pdf")
async def export_pdf():
    """
    Export all breed data to a downloadable PDF file.
    """
    try:
        pdf_bytes = await export_breeds_pdf()
        if not pdf_bytes:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF generation failed",
            )

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=breeds.pdf"},
        )
    except Exception as e:
        logger.error("PDF export failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while exporting PDF",
        )

@router.post("/analyze-image")
async def analyze_image_from_url(image_url: Optional[str] = Form(None)):
    if not image_url:
        raise HTTPException(status_code=400, detail="Image URL is required.")

    result = await analyze_image_url(image_url)
    if result.startswith("OpenAI API error"):
        raise HTTPException(status_code=500, detail=result)

    return {"analysis": result}

@router.post("/breeds/match")
async def match_breed(request: BreedMatchRequest):
    result = await match_best_breed(request.preferences)
    return {"match": result}