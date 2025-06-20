from fastapi import APIRouter, Depends, HTTPException, Request
from src.auth.auth_router import get_current_user
from transformers import pipeline
from src.database import save_analysis
from src.services.redis_service import get_cache, set_cache
import json
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/classify", tags=["classify"])

class ClassifyRequest(BaseModel):
    text: str
    labels: List[str] = None

class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    all_categories: List[str]
    all_confidences: List[float]
    text: str

# Pipeline de classificação zero-shot em inglês
classifier_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

RATE_LIMIT = 10

@router.post("/", response_model=ClassifyResponse)
def classify_text(request: ClassifyRequest, user: dict = Depends(get_current_user), req: Request = None):
    ip = req.client.host if req else "unknown"
    key = f"rl:classify:{ip}"
    count = get_cache(key) or 0
    if count and int(count) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    set_cache(key, int(count) + 1, expire_seconds=60)
    text = request.text
    # Exemplos de labels, pode ser customizado conforme o caso de uso
    candidate_labels = request.labels or ["news", "sports", "politics", "technology", "entertainment"]
    cache_key = f"classify:{text}:{','.join(candidate_labels)}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    result_raw = classifier_pipeline(text, candidate_labels)
    result = {
        "category": result_raw["labels"][0],
        "confidence": float(result_raw["scores"][0]),
        "all_categories": result_raw["labels"],
        "all_confidences": [float(s) for s in result_raw["scores"]],
        "text": text
    }
    # Salva no banco de dados
    save_analysis(
        user_id=user.get("username", "anonymous"),
        input_text=text,
        analysis_type="classification",
        result=json.dumps(result)
    )
    set_cache(cache_key, result)
    return result
