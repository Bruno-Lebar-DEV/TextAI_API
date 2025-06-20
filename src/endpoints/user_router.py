from fastapi import APIRouter, HTTPException, Depends
from src.services.crypto_service import hash_password, verify_password
from src.database import get_connection
from src.auth.auth_router import authenticate_user, create_access_token, get_current_user
import psycopg2
from datetime import timedelta
import logging
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class UserRegisterRequest(BaseModel):
    username: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserListResponse(BaseModel):
    id: int
    username: str
    created_at: str

@router.post("/register", response_model=UserRegisterResponse)
def register_user(user: UserRegisterRequest):
    username = user.username
    password = user.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    password_hash = hash_password(password)
    try:
        conn = get_connection()
    except UnicodeDecodeError as e:
        logging.error(f"Erro de encoding ao conectar ao banco: {e}")
        raise HTTPException(status_code=500, detail="Erro de encoding ao conectar ao banco. Verifique se as variáveis de ambiente e o banco estão em UTF-8 e sem acentos.")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                raise HTTPException(status_code=409, detail="Username already exists.")
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;",
                (username, password_hash)
            )
            conn.commit()
            return {"message": "User registered successfully."}
    finally:
        conn.close()

@router.post("/login", response_model=UserLoginResponse)
def login_user(user: UserLoginRequest):
    try:
        user_db = authenticate_user(user.username, user.password)
    except UnicodeDecodeError as e:
        logging.error(f"Erro de encoding ao conectar ao banco: {e}")
        raise HTTPException(status_code=500, detail="Erro de encoding ao conectar ao banco. Verifique se as variáveis de ambiente e o banco estão em UTF-8 e sem acentos.")
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=list[UserListResponse])
def list_users(current_user: dict = Depends(get_current_user)):
    try:
        conn = get_connection()
    except UnicodeDecodeError as e:
        logging.error(f"Erro de encoding ao conectar ao banco: {e}")
        raise HTTPException(status_code=500, detail="Erro de encoding ao conectar ao banco. Verifique se as variáveis de ambiente e o banco estão em UTF-8 e sem acentos.")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, created_at FROM users ORDER BY id;")
            users = cur.fetchall()
            # Serializa created_at para string
            for u in users:
                if u["created_at"] is not None:
                    u["created_at"] = u["created_at"].isoformat()
            return users
    finally:
        conn.close()
