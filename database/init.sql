-- Script de inicialização do banco de dados para o TextAI_API
-- Execute este script conectado como superusuário ou com permissões suficientes

-- Criação do banco de dados (execute apenas se ainda não existir)
-- CREATE DATABASE textaidb;

-- Criação do usuário (execute apenas se ainda não existir)
-- CREATE USER spostgres WITH PASSWORD 'psql123';

-- Conceder permissões ao usuário
-- GRANT ALL PRIVILEGES ON DATABASE textaidb TO spostgres;

-- Conectar ao banco de dados
\c textaidb;

-- Tabela para armazenar análises de texto
CREATE TABLE IF NOT EXISTS text_analysis (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64),
    input_text TEXT NOT NULL,
    analysis_type VARCHAR(32) NOT NULL, -- sentiment, summary, classification
    result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para usuários (opcional, para autenticação futura)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
