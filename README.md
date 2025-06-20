# TextAI_API 🤖📝  

## 📌 Visão Geral  
O **TextAI_API** é uma **API especializada em processamento de textos**, capaz de **analisar sentimentos, gerar resumos automáticos e classificar textos**, utilizando técnicas avançadas de **Natural Language Processing (NLP)**. O projeto foca na **escalabilidade**, **segurança** e **eficiência** na manipulação de linguagem, proporcionando insights valiosos a partir de textos.  

---

## 🔥 Principais Funcionalidades  
✔️ **Análise de Sentimentos:** Detecta emoções e polaridade de textos.  
✔️ **Geração de Resumos Automáticos:** Extrai os principais pontos de um texto longo.  
✔️ **Classificação de Texto:** Organiza conteúdos por categorias com NLP.  
✔️ **Autenticação Segura:** Proteção com **OAuth2** ou **JWT**.  
✔️ **Caching e Otimização:** Uso de **Redis** para armazenamento temporário eficiente.  
✔️ **Testes Automatizados:** Garantia de estabilidade com **Pytest**.  
✔️ **Histórico de Análises:** Consulta dos resultados anteriores por usuário.  

---

## 🚀 Tecnologias Utilizadas  

### *⚙ Back-end*  
- **FastAPI (Python)** → Framework rápido e escalável para APIs.  
- **PostgreSQL** → Banco de dados otimizado para armazenar textos analisados.  

### *🤖 NLP & Machine Learning*  
- **SpaCy** → Processamento eficiente de linguagem natural.  
- **Transformers (Hugging Face)** → Modelos pré-treinados para análise avançada.  

### *🔐 Segurança e Performance*  
- **OAuth2 + JWT** → Autenticação robusta contra acessos indevidos.  
- **Redis** → Cache eficiente para consultas rápidas.  

### *🛠️ Testes e Otimização*  
- **Pytest** → Framework para testes automatizados.  
- **Locust** → Testes de carga/performance.  

---

## 📂 Estrutura do Repositório  
```bash
📦 TextAI_API
 ├── 📂 src/            # Código principal da API
 │   ├── endpoints/     # Lógica dos endpoints
 │   ├── models/        # Modelos de dados
 │   ├── services/      # Processamento de NLP e lógica de negócios
 │   ├── auth/          # Autenticação via JWT e OAuth2
 │   ├── caching/       # Configuração de Redis
 │   ├── tests/         # Testes unitários e de integração
 │   ├── main.py        # Arquivo principal do FastAPI
 ├── 📂 docs/           # Documentação técnica
 ├── 📂 database/       # Scripts de banco de dados
 ├── 📜 README.md       # Documento de apresentação do projeto
 ├── 📜 LICENSE         # Licença de código aberto
 ├── 📜 .gitignore      # Arquivos que devem ser ignorados no repositório
 ├── requirements.txt   # Dependências do projeto
 ├── locustfile.py      # Script de teste de carga
```  

---

## ✅ Checklist de Desenvolvimento  

- [x] **Planejamento**  
  - [x] Definir requisitos e funcionalidades principais.  
  - [x] Mapear fluxos de análise de texto e processamento NLP.  
- [x] **Configuração do Ambiente**  
  - [x] Instalar dependências do Python e FastAPI.  
  - [x] Configurar banco de dados e sistema de cache.  
  - [x] Implementar autenticação via OAuth2 ou JWT.  
- [x] **Desenvolvimento do Back-end**  
  - [x] Criar endpoints para análise de sentimentos, resumos automáticos e classificação.  
  - [x] Implementar integração com modelos pré-treinados via Hugging Face.  
- [x] **Testes e Otimizações**  
  - [x] Implementar caching com Redis para consultas rápidas.  
  - [x] Criar testes unitários e de integração com Pytest.  
  - [x] Realizar testes de carga/performance (Locust).  
- [ ] **Deploy e Integração**  
  - [ ] Configurar CI/CD para deploy automatizado.  
  - [ ] Realizar testes finais de performance e escalabilidade.  

---

## 🔧 Como Rodar o Projeto  

### **Pré-requisitos**  
Antes de iniciar, certifique-se de ter instalado:  
- [Python 3.8+](https://www.python.org/downloads/)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [PostgreSQL](https://www.postgresql.org/download/)  
- [Redis](https://redis.io/download)  
- [Git](https://git-scm.com/downloads)  

### **1️⃣ Clonar o Repositório**  
```bash
# Clone o repositório e acesse a pasta
 git clone https://github.com/seu-usuario/TextAI_API.git
 cd TextAI_API
```

### **2️⃣ Instalar Dependências**  
```bash
# Ative o ambiente virtual e instale as dependências
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### **3️⃣ Configurar Banco de Dados e Cache**  
```bash
# Inicie o PostgreSQL e o Redis
# Crie o banco e usuário conforme docs/comandos_projeto.md
psql -U spostgres -d textaidb -f database/init.sql
redis-server
```

### **4️⃣ Configurar variáveis de ambiente**
- Copie o arquivo `.env.example` para `.env.local` e ajuste as variáveis conforme seu ambiente.

### **5️⃣ Executar a API**  
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### **6️⃣ Testar a API**
- Acesse a documentação interativa: http://localhost:8000/docs
- Execute os testes automatizados:
```bash
pytest tests/
```
- (Opcional) Execute testes de carga:
```bash
locust -f locustfile.py --host http://localhost:8000
```

Agora o **TextAI_API** está pronto para análise e processamento de textos! 🚀  

---

## 🚀 Contribuições  

Quer colaborar com o **TextAI_API**? Qualquer melhoria é bem-vinda!  

### 🔹 Como contribuir  
1. **Fork o repositório** para ter uma cópia no seu GitHub.  
2. **Crie uma nova branch** para suas melhorias:  
   ```bash
   git checkout -b minha-feature
   ```
3. **Implemente suas alterações**, seguindo as boas práticas do projeto.  
4. **Faça um commit das suas mudanças:**  
   ```bash
   git commit -m "feat: descrição da melhoria"
   ```
5. **Envie para o seu repositório e abra um Pull Request:**  
   ```bash
   git push origin minha-feature
   ```
6. **Aguarde revisão e sugestões! 🚀**  

🎯 Sugestões de contribuição:  
✔️ **Correção de bugs**  
✔️ **Melhorias na performance**  
✔️ **Novas funcionalidades (ex. mais modelos de NLP)**  
✔️ **Refatoração do código**  
✔️ **Melhorias na segurança e autenticação**  

---

## 📄 Licença  

Este projeto está sob a licença MIT, permitindo colaboração aberta! 📝
