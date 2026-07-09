from app.utils.logger import logger

class BehaviourService:
    def analyze_behaviour(self, data: dict):
        logger.info("Analyzing sales representative activity patterns (placeholder)...")
        # Mock analysis response
        return {
            "average_response_time_hours": 2.5,
            "follow_up_frequency_days": 1.7,
            "communication_tone": "PROFESSIONAL",
            "activity_completion_rate": 0.85,
            "suggested_actions": ["Increase touchpoints with customer via email", "Schedule a follow-up demo meeting"]
        }

behaviour_service = BehaviourService()
