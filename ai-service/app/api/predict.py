from fastapi import APIRouter, HTTPException
from app.schemas.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Predict deal closure success and risk")
async def predict_deal(request: PredictionRequest):
    try:
        result = prediction_service.predict_deal_success(
            deal_amount=request.deal_amount,
            deal_stage=request.deal_stage,
            activities_count=request.activities_count,
            email_sentiment_score=request.email_sentiment_score,
            average_response_time_hours=request.average_response_time_hours
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deal prediction failed: {str(e)}")
