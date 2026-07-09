# 🤖 SalesPulse AI Microservice

> **Enterprise FastAPI Microservice for B2B Sales Sentiment, Behaviour Analytics, and Deal Win Probability**

This microservice acts as the AI/ML analytics engine for the SalesPulse platform, exposing endpoints for sentiment analysis of communications, behavioural patterns processing, win-rate predictions, and rep coaching advice.

---

## 🏗️ Folder Structure

```text
ai-service/
│
├── app/
│   ├── api/                   # Router endpoints definitions
│   │   ├── sentiment.py
│   │   ├── behaviour.py
│   │   ├── predict.py
│   │   └── recommend.py
│   │
│   ├── config/
│   │   └── config.py          # Env settings parsing
│   │
│   ├── core/                  # Core modules configurations
│   │
│   ├── models/                # Saved custom model artifacts (.joblib, .pt)
│   │
│   ├── schemas/               # Request/Response validation schemas
│   │   └── schemas.py
│   │
│   ├── services/              # Inference orchestrations and analytics business logic
│   │   ├── sentiment_service.py
│   │   ├── behaviour_service.py
│   │   ├── prediction_service.py
│   │   └── recommendation_service.py
│   │
│   ├── utils/                 # Diagnostic and loader utilities
│   │   ├── logger.py
│   │   ├── model_loader.py
│   │   ├── response_formatter.py
│   │   └── text_cleaner.py
│   │
│   └── main.py                # Service initialization, lifespan settings, & CORS mapping
│
├── .env                       # Local environment configurations
├── requirements.txt           # Python library requirements
└── README.md                  # Developer integration documentation
```

---

## 🛠️ Setup & Execution

### 1. Install System Requirements
Ensure Python 3.10+ is installed on your machine.

### 2. Install Packages
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Configure `ai-service/.env`:
```env
MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
DEVICE=cpu
PORT=8000
```

### 4. Start the Uvicorn Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Once booted, the server and interactive documentation will be available at:
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Documentation

| Endpoint | Method | Payload Type | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | None | Health Check API |
| `/sentiment` | `POST` | `SentimentRequest` | Sentiment scoring of text/emails (runs HF inference) |
| `/behaviour` | `POST` | `dict` | Evaluates response frequency & communication tone |
| `/predict` | `POST` | `PredictionRequest` | Win rate prediction probability & risk level scoring |
| `/recommend` | `POST` | `RecommendationRequest` | Actionable coaching tips generation |

---

## 💡 AI/ML Model Design Choices

1. **Lifespan Model Loading**: The sentiment model (`distilbert-base-uncased-finetuned-sst-2-english`) is downloaded and cached during the FastAPI `lifespan` startup hook. This ensures zero cold-start latency for the first analysis request.
2. **Device Adaptive Execution**: Auto-detects if a CUDA-enabled GPU is available. It defaults to CPU running but supports GPU scaling by changing `DEVICE=cuda` in `.env`.
3. **Pydantic Validation**: All endpoints enforce strict request and response schema models, ensuring payload alignment with the node.js gateway.
