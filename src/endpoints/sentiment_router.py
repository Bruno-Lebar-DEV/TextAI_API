from fastapi import APIRouter, Depends, HTTPException, Request
from src.auth.auth_router import get_current_user
from transformers import pipeline
from src.database import save_analysis
from src.services.redis_service import get_cache, set_cache
import json
from pydantic import BaseModel
import time

router = APIRouter(prefix="/sentiment", tags=["sentiment"])

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    text: str

# Pipeline padrão de análise de sentimentos em inglês
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

RATE_LIMIT = 10  # requisições por minuto

@router.post("/", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest, user: dict = Depends(get_current_user), req: Request = None):
    # Rate limiting simples por IP
    ip = req.client.host if req else "unknown"
    key = f"rl:sentiment:{ip}"
    count = get_cache(key) or 0
    if count and int(count) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    set_cache(key, int(count) + 1, expire_seconds=60)
    text = request.text
    cache_key = f"sentiment:{text}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    result_raw = sentiment_pipeline(text)[0]
    result = {
        "sentiment": result_raw["label"],
        "confidence": float(result_raw["score"]),
        "text": text
    }
    # Salva no banco de dados
    save_analysis(
        user_id=user.get("username", "anonymous"),
        input_text=text,
        analysis_type="sentiment",
        result=json.dumps(result)
    )
    set_cache(cache_key, result)
    return result
