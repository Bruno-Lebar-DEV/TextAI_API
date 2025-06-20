from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from src.services.crypto_service import hash_password, verify_password
from src.database import get_connection

# Carrega variáveis do .env.local
load_dotenv()

# Configurações
SECRET_KEY = os.getenv("JWT_SECRET", "local_secret_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])

def authenticate_user(username: str, password: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username, password_hash FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            if not user or not verify_password(password, user["password_hash"]):
                return False
            return user
    finally:
        conn.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Busca usuário no banco de dados
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users WHERE username=%s", (username,))
            user = cur.fetchone()
            if user is None:
                raise credentials_exception
            return user
    finally:
        conn.close()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate-token")
def validate_token(current_user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Remove a chave 'exp' se não quiser mostrar a expiração
    token_info = {k: v for k, v in payload.items() if k != 'exp'}
    token_info['exp'] = payload.get('exp')
    return {"token_info": token_info, "user": current_user}
