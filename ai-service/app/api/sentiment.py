from fastapi import APIRouter, HTTPException
from app.schemas.schemas import SentimentRequest, SentimentResponse
from app.services.sentiment_service import sentiment_service

router = APIRouter()

@router.post("/sentiment", response_model=SentimentResponse, summary="Analyze text/email sentiment")
async def analyze_sentiment(request: SentimentRequest):
    try:
        result = sentiment_service.analyze_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment processing failed: {str(e)}")
