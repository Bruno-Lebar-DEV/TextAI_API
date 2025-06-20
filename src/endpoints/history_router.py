from fastapi import APIRouter, Depends, HTTPException
from src.auth.auth_router import get_current_user
from src.database import get_connection
from typing import List

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=List[dict])
def get_history(user: dict = Depends(get_current_user)):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, input_text, analysis_type, result, created_at FROM text_analysis WHERE user_id=%s ORDER BY created_at DESC LIMIT 100;", (user["username"],))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()
