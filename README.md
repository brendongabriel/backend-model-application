
# 🔧 Backend — Serviço de Análise de Variáveis de Produção

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Status](https://img.shields.io/badge/Status-Ativo-success)
![Tests](https://img.shields.io/badge/Pytest-Coberto-orange?logo=pytest)

Backend intermediário entre o **frontend** e o **serviço de modelo**, responsável por:

- Gerenciar máquinas cadastradas
- Controlar o envio de dados de treino via CSV
- Repassar resultados do modelo para o frontend
- Armazenar estado, métricas e resultados no banco PostgreSQL
- Servir APIs REST limpas para o painel web

Esse Backend serve para dar autonomia de utilizar os retornos do modelo da melhor forma e tratar os dados para o frontend

---

# 📌 **1. Arquitetura Geral**

Aqui nesse repositório, estamos na camada Backend, como é possivel visualizar na imagem abaixo

<p align="center">
  <img src="./docs/arquitetura.png" width="450">
</p>

---

# 📦 **2. Estrutura do Projeto**

```
backend/
│── app/
│   ├── main.py          # Rotas FastAPI
│   ├── db.py            # Conexão e ORM
│   ├── models.py        # Schemas SQLAlchemy
│   ├── services/        # Integrações externas
│   └── utils/           # Helpers
│
│── tests/
│   ├── test_api.py
│   └── test_services.py
│
│── docs/
│   └── arquitetura.png
│
├── requirements.txt
└── README.md
```

---

# 🚀 **3. Como Rodar Localmente**

### 🔹 1. Criar ambiente
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 🔹 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 🔹 3. Configurar variáveis de ambiente

Crie `.env`:

```
DATABASE_URL=postgresql://user:pass@localhost:5432/modeldb
RELEVANCE_SERVICE_API_URL=http://127.0.0.1:8000
```

### 🔹 4. Iniciar o backend
```bash
uvicorn app.main:app  --port 8001 --reload
```

API disponível em:

📍 **http://localhost:8001**

---

# ⚙️ **4. Principais APIs**

- POST /models/
- POST /train/
- GET /ranking/
- GET /models/
- DELETE /models/{id}

---

# 🧠 **5. Fluxo de Treinamento**

<p align="center">
  <img src="./docs/pipeline.png" width="450">
</p>



# 🧪 **6. Testes**

Rodar testes:

```bash
pytest -v
```

O backend possui testes para:

✔ CRUD das máquinas  
✔ Rotas principais  
✔ Integração com serviço do modelo (mockado)

---

# 📝 **8. Referências**

- FASTAPI — Documentação Oficial  
- PostgreSQL — Guia de Desenvolvimento  
- Uvicorn — Servidor ASGI  
- SHAP — Interpretação de Modelos  
- Scikit-Learn — RandomForestRegressor

---

# 🎯 **9. Status**

Este backend funciona como um **núcleo de integração**, conectando:

🔗 **Frontend** → Dashboard  
🔗 **Backend** → Rotas REST  
🔗 **Modelo** → Treinamento e ranking  
🔗 **Banco** → Armazenamento persistente  

Ideal para aplicações industriais que precisam **entender quais variáveis impactam sua produção**.
