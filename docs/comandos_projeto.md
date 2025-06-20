# Comandos Essenciais do Projeto TextAI_API

## 1. PostgreSQL

### 1.1. Acessar o terminal do PostgreSQL
```
psql -U postgres
```

### 1.2. Criar banco de dados e usuário (ajuste conforme necessário)
```
CREATE DATABASE textai_db;
CREATE USER spostgres WITH PASSWORD 'psql123';
GRANT ALL PRIVILEGES ON DATABASE textai_db TO spostgres;
```

### 1.3. Conectar ao banco criado
```
\c textai_db
```

### 1.4. Executar script de criação de tabelas
No terminal do psql já conectado ao banco:
```
\i database/init.sql
```

---

## 2. Redis

### 2.1. Iniciar o servidor Redis (Windows)
```
redis-server
```

---

## 3. Python e Projeto

### 3.1. Criar e ativar ambiente virtual
```
python -m venv .venv
.venv\Scripts\activate
```

### 3.2. Instalar dependências
```
pip install -r requirements.txt
```

### 3.3. Rodar a API em modo desenvolvimento
```
uvicorn src.main:app --reload
```

### 3.4. Visualizar serviços rodando
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Redis: http://localhost:6379 (CLI)
- PostgreSQL: via psql ou pgAdmin

### 3.5. Instalar/atualizar dependências específicas (exemplo)
```
pip install --upgrade bcrypt passlib psycopg2-binary transformers fastapi[all] python-dotenv redis
```

---

## 4. Dicas Úteis

- Para listar processos Python rodando (Windows):
```
tasklist /FI "IMAGENAME eq python.exe"
```
- Para matar um processo pelo PID:
```
taskkill /PID <PID> /F
```
- Para garantir encoding UTF-8 no .env, salve o arquivo como UTF-8 (sem BOM) em seu editor.

---

Esses comandos cobrem o ciclo de vida do projeto: banco, cache, dependências, execução e troubleshooting.
