from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.auth_router import router as auth_router
from src.endpoints.sentiment_router import router as sentiment_router
from src.endpoints.summary_router import router as summary_router
from src.endpoints.classify_router import router as classify_router
from src.endpoints.user_router import router as user_router
from src.endpoints.history_router import router as history_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sentiment_router)
app.include_router(summary_router)
app.include_router(classify_router)
app.include_router(user_router)
app.include_router(history_router)

@app.get("/")
def read_root():
    return {"message": "TextAI_API está rodando!"}
