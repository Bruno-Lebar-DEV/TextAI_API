-- Comando para recriar o banco de dados e o usuário do zero
-- Execute no terminal do psql como superusuário

-- 1. Desconecte todos os usuários do banco, se necessário
-- SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'textaidb';

-- 2. Drop banco e usuário antigos (se existirem)
DROP DATABASE IF EXISTS textaidb;
DROP USER IF EXISTS textaiuser;

-- 3. Crie o banco e o usuário
CREATE DATABASE textaidb ENCODING 'UTF8';
CREATE USER textaiuser WITH PASSWORD 'textai_pass_2025';
GRANT ALL PRIVILEGES ON DATABASE textaidb TO textaiuser;

-- 4. Conecte ao banco e crie as tabelas
\c textaidb
\i database/init.sql
