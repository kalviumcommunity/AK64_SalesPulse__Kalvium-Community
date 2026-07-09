from fastapi import APIRouter, HTTPException
from app.services.behaviour_service import behaviour_service

router = APIRouter()

@router.post("/behaviour", summary="Analyze sales activity and communication behaviour patterns")
async def analyze_behaviour(request: dict):
    try:
        result = behaviour_service.analyze_behaviour(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behaviour analysis failed: {str(e)}")
