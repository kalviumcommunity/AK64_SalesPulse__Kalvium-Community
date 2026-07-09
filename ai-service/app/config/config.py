import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

class Settings:
    MODEL_NAME: str = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
    DEVICE: str = os.getenv("DEVICE", "cpu")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"

settings = Settings()
