from fastapi import APIRouter, Depends, HTTPException, Request
from src.auth.auth_router import get_current_user
from transformers import pipeline
from src.database import save_analysis
from src.services.redis_service import get_cache, set_cache
import json
from pydantic import BaseModel

router = APIRouter(prefix="/summary", tags=["summary"])

class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    text: str

# Pipeline de sumarização em inglês
summary_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

RATE_LIMIT = 10

@router.post("/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, user: dict = Depends(get_current_user), req: Request = None):
    ip = req.client.host if req else "unknown"
    key = f"rl:summary:{ip}"
    count = get_cache(key) or 0
    if count and int(count) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    set_cache(key, int(count) + 1, expire_seconds=60)
    text = request.text
    cache_key = f"summary:{text}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    summary_raw = summary_pipeline(text, max_length=130, min_length=30, do_sample=False)[0]
    result = {
        "summary": summary_raw["summary_text"],
        "text": text
    }
    # Salva no banco de dados
    save_analysis(
        user_id=user.get("username", "anonymous"),
        input_text=text,
        analysis_type="summary",
        result=json.dumps(result)
    )
    set_cache(cache_key, result)
    return result
