import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
from app.utils.model_loader import model_loader
from app.utils.logger import logger

# Import API Routers
from app.api import sentiment, behaviour, predict, recommend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up SalesPulse AI Service...")
    
    # Load the Hugging Face model in a background thread to prevent blocking FastAPI boot
    def load_model_background():
        try:
            model_loader.load_sentiment_model()
        except Exception as e:
            logger.error(f"Error during background model loading: {e}")
            logger.warning("Sentiment analysis inference will fallback to mock responses.")

    logger.info("Spawning background thread to load Hugging Face sentiment model...")
    thread = threading.Thread(target=load_model_background, daemon=True)
    thread.start()
    
    yield
    # Shutdown actions
    logger.info("Shutting down SalesPulse AI Service...")

app = FastAPI(
    title="SalesPulse AI Service",
    description="Microservice providing B2B sales behaviour analysis, win probability prediction, and AI recommendation engines.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Endpoint Routers
app.include_router(sentiment.router, tags=["Sentiment Analysis"])
app.include_router(behaviour.router, tags=["Behaviour Analysis"])
app.include_router(predict.router, tags=["Deal Prediction"])
app.include_router(recommend.router, tags=["Recommendation Engine"])

# Health Check Route
@app.get("/", summary="Health Check API")
async def health_check():
    return {
        "status": "running",
        "service": "SalesPulse AI Service"
    }
