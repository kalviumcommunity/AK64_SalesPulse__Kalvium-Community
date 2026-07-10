from transformers import pipeline
from app.config.config import settings
from app.utils.logger import logger
import torch

class ModelLoader:
    def __init__(self):
        self.sentiment_pipeline = None

    def load_sentiment_model(self):
        if self.sentiment_pipeline is None:
            logger.info(f"Loading sentiment model: {settings.MODEL_NAME} on device: {settings.DEVICE}")
            device = 0 if settings.DEVICE == "cuda" and torch.cuda.is_available() else -1
            try:
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=settings.MODEL_NAME,
                    device=device
                )
                logger.info("Sentiment model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load sentiment model: {e}")
                raise e
        return self.sentiment_pipeline

model_loader = ModelLoader()
