from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class SentimentRequest(BaseModel):
    text: str = Field(..., description="The input text (such as email body) to analyze.")

class SentimentResponse(BaseModel):
    sentiment: str = Field(..., description="The predicted sentiment label (e.g. POSITIVE, NEUTRAL, NEGATIVE).")
    score: float = Field(..., description="The confidence score of the sentiment prediction.")

class PredictionRequest(BaseModel):
    deal_amount: float = Field(..., description="The total transaction value of the deal.")
    deal_stage: str = Field(..., description="The current sales pipeline stage of the deal.")
    activities_count: int = Field(0, description="Total number of logged sales activities.")
    email_sentiment_score: float = Field(0.0, description="Aggregated average email sentiment score.")
    average_response_time_hours: float = Field(0.0, description="Average response delay in hours.")

class PredictionResponse(BaseModel):
    success_probability: float = Field(..., description="The predicted probability of closing the deal successfully.")
    risk_level: str = Field(..., description="Identified risk level associated with the deal.")
    prediction_details: Optional[Dict[str, Any]] = Field(None, description="Metadata or features driving this prediction.")

class RecommendationRequest(BaseModel):
    salesperson_id: str = Field(..., description="The unique ID of the sales representative.")
    deal_id: str = Field(..., description="The unique ID of the target deal.")
    sentiment_history: Optional[List[Dict[str, Any]]] = Field(None, description="Recent history of email sentiments.")
    activities_summary: Optional[Dict[str, Any]] = Field(None, description="Summary counts of activity types.")

class RecommendationResponse(BaseModel):
    recommendation: str = Field(..., description="Personalized AI-powered coaching advice.")
    priority: str = Field(..., description="Action priority level: HIGH, MEDIUM, LOW.")
    suggested_action: str = Field(..., description="Concrete action step recommended for the representative.")
