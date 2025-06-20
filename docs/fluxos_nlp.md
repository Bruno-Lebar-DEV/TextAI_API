# Fluxos de Análise de Texto e Processamento NLP

Este documento descreve, passo a passo, o fluxo de dados e processamento dentro do TextAI_API para cada funcionalidade principal.

---

## 1. Fluxo Geral (para qualquer endpoint)
1. **Recepção da Requisição:**
   - O usuário envia uma requisição HTTP (POST) para o endpoint desejado, contendo o texto e, se necessário, o token de autenticação.
2. **Autenticação:**
   - O sistema valida o token JWT/OAuth2. Se inválido, retorna erro de autenticação.
3. **Verificação de Cache:**
   - O sistema verifica se o resultado para aquele texto já está em cache (Redis).
   - Se sim, retorna o resultado imediatamente.
4. **Processamento NLP:**
   - Se não houver cache, o texto é processado conforme o endpoint:
     - Análise de sentimentos
     - Geração de resumo
     - Classificação de texto
5. **Armazenamento:**
   - O resultado é salvo no banco de dados PostgreSQL.
   - O resultado também é salvo no cache Redis para futuras consultas rápidas.
6. **Resposta:**
   - O sistema retorna o resultado ao usuário em formato JSON.

---

## 2. Fluxo Específico: Análise de Sentimentos
1. Recebe texto via endpoint `/sentiment`.
2. Valida autenticação.
3. Verifica cache.
4. Usa modelo NLP (ex: SpaCy, Transformers) para identificar polaridade e emoção.
5. Salva resultado no banco e cache.
6. Retorna resposta ao usuário.

## 3. Fluxo Específico: Geração de Resumos
1. Recebe texto via endpoint `/summarize`.
2. Valida autenticação.
3. Verifica cache.
4. Usa modelo de sumarização (ex: Transformers) para gerar resumo.
5. Salva resultado no banco e cache.
6. Retorna resposta ao usuário.

## 4. Fluxo Específico: Classificação de Texto
1. Recebe texto via endpoint `/classify`.
2. Valida autenticação.
3. Verifica cache.
4. Usa modelo de classificação para categorizar o texto.
5. Salva resultado no banco e cache.
6. Retorna resposta ao usuário.

---

Esses fluxos garantem eficiência, segurança e rastreabilidade em todas as operações do TextAI_API.
