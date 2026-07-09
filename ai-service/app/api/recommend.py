from fastapi import APIRouter, HTTPException
from app.schemas.schemas import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import recommendation_service

router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse, summary="Generate sales representative coaching recommendations")
async def generate_recommendation(request: RecommendationRequest):
    try:
        result = recommendation_service.generate_coaching_recommendation(
            salesperson_id=request.salesperson_id,
            deal_id=request.deal_id,
            sentiment_history=request.sentiment_history,
            activities_summary=request.activities_summary
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
