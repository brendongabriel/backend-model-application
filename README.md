
# 🔧 Backend — Serviço de Análise de Variáveis de Produção

1. [Repositório do backend da aplicação;](https://github.com/brendongabriel/backend-model-application)
2. [Repositório do frontend da aplicação;](https://github.com/brendongabriel/frontend-model-application)

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
│── docs/
│   └── arquitetura.png
│
├── requirements.txt
└── README.md
```

---


# ⚙️ **4. Principais APIs**

- POST /machines/ - criação da máquina e criação do modelo
- POST /train/ - treinamento do modelo
- POST /webhook/treinamento/ - recebimento do treinamento do modelo
- GET /ranking/ - busca do ranking da maquina
- GET /machines/ - busca das maquinas
- DELETE /machines/{id} - deletar as maquinas

<details>
  <summary><strong>openapi.json</strong></summary>

```json
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/machines/": {
            "get": {
                "summary": "List Machines",
                "operationId": "list_machines_machines__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "items": {
                                        "$ref": "#/components/schemas/Machine"
                                    },
                                    "type": "array",
                                    "title": "Response List Machines Machines  Get"
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create Machine",
                "operationId": "create_machine_machines__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/MachineCreate"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Machine"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/machines/{machine_id}": {
            "delete": {
                "summary": "Delete Machine",
                "operationId": "delete_machine_machines__machine_id__delete",
                "parameters": [
                    {
                        "name": "machine_id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer",
                            "title": "Machine Id"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/train/": {
            "post": {
                "summary": "Train Model",
                "operationId": "train_model_train__post",
                "parameters": [
                    {
                        "name": "machine_id",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "integer",
                            "title": "Machine Id"
                        }
                    },
                    {
                        "name": "target_column",
                        "in": "query",
                        "required": true,
                        "schema": {
                            "type": "string",
                            "title": "Target Column"
                        }
                    }
                ],
                "requestBody": {
                    "required": true,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_train_model_train__post"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/webhook/treinamento/": {
            "post": {
                "summary": "Webhook Treinamento",
                "operationId": "webhook_treinamento_webhook_treinamento__post",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/ranking/": {
            "get": {
                "summary": "Get Ranking",
                "operationId": "get_ranking_ranking__get",
                "parameters": [
                    {
                        "name": "machine_id",
                        "in": "query",
                        "required": false,
                        "schema": {
                            "type": "integer",
                            "title": "Machine Id"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Body_train_model_train__post": {
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "title": "File"
                    }
                },
                "type": "object",
                "required": [
                    "file"
                ],
                "title": "Body_train_model_train__post"
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        },
                        "type": "array",
                        "title": "Detail"
                    }
                },
                "type": "object",
                "title": "HTTPValidationError"
            },
            "Machine": {
                "properties": {
                    "machine_name": {
                        "type": "string",
                        "title": "Machine Name"
                    },
                    "id": {
                        "type": "integer",
                        "title": "Id"
                    },
                    "status": {
                        "type": "string",
                        "title": "Status"
                    },
                    "model_id": {
                        "type": "integer",
                        "title": "Model Id"
                    }
                },
                "type": "object",
                "required": [
                    "machine_name",
                    "id",
                    "status",
                    "model_id"
                ],
                "title": "Machine"
            },
            "MachineCreate": {
                "properties": {
                    "machine_name": {
                        "type": "string",
                        "title": "Machine Name"
                    }
                },
                "type": "object",
                "required": [
                    "machine_name"
                ],
                "title": "MachineCreate"
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "integer"
                                }
                            ]
                        },
                        "type": "array",
                        "title": "Location"
                    },
                    "msg": {
                        "type": "string",
                        "title": "Message"
                    },
                    "type": {
                        "type": "string",
                        "title": "Error Type"
                    }
                },
                "type": "object",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "title": "ValidationError"
            }
        }
    }
}
```
</details> 
---

# 🚀 **3. Como Rodar Localmente**

### 🔹 1. Configurar variáveis de ambiente

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

# 🧠 **5. Fluxo de Treinamento**

<p align="center">
  <img src="./docs/pipeline.png" width="450">
</p>


# 📝 **8. Referências**

- FASTAPI — Documentação Oficial  
- PostgreSQL — Guia de Desenvolvimento  
- Uvicorn — Servidor ASGI 

---

# 🎯 **9. Status**

Este backend funciona como um **núcleo de integração**, conectando:

🔗 **Frontend** → Dashboard  
🔗 **Backend** → Rotas REST  
🔗 **Modelo** → Treinamento e ranking  
🔗 **Banco** → Armazenamento persistente  

Ideal para aplicações industriais que precisam **entender quais variáveis impactam sua produção**.
