from app.utils.model_loader import model_loader
from app.utils.text_cleaner import clean_text
from app.utils.logger import logger

class SentimentService:
    def analyze_text(self, text: str):
        cleaned = clean_text(text)
        logger.info(f"Analyzing sentiment for text snippet: {cleaned[:60]}...")
        
        # Load the pipeline from ModelLoader
        pipeline = model_loader.sentiment_pipeline
        if pipeline:
            try:
                # Perform inference
                result = pipeline(cleaned)[0]
                label = result["label"].upper()
                score = float(result["score"])
                
                # Standardize binary outputs if needed (e.g., LABEL_1/LABEL_0)
                if label == "LABEL_1" or "POSITIVE" in label:
                    return {"sentiment": "POSITIVE", "score": score}
                elif label == "LABEL_0" or "NEGATIVE" in label:
                    return {"sentiment": "NEGATIVE", "score": score}
                else:
                    return {"sentiment": label, "score": score}
            except Exception as e:
                logger.error(f"Failed to perform sentiment analysis inference: {e}")
        
        # Mock fallback response
        return {"sentiment": "POSITIVE", "score": 0.88}

sentiment_service = SentimentService()
