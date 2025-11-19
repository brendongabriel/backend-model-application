# app/main.py
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
from app.model_service import cadastrar_maquina, remover_maquina, treinar_modelo, obter_ranking

app = FastAPI(title="Machine Management API")

app = FastAPI()

# Cors local
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.13:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,       
    allow_methods=["*"],          
    allow_headers=["*"],          
)


# Dependência de banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar uma nova máquina
@app.post("/machines/", response_model=schemas.Machine)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db)):
    try:
        # Chama o serviço de cadastro da máquina
        response_service = cadastrar_maquina(machine.machine_name)
        if "error" in response_service: 
            raise HTTPException(status_code=400, detail=f"Erro ao cadastrar a máquina: {response_service['error']}")
        
        # Se o serviço de cadastro for bem-sucedido, cria no banco de dados
        db_machine = models.Machine(machine_name=machine.machine_name, status="created", model_id=response_service["model_id"])
        db.add(db_machine)
        db.commit()
        db.refresh(db_machine)

        return db_machine

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao cadastrar a máquina: {str(e)}")

# Listar todas as máquinas
@app.get("/machines/", response_model=list[schemas.Machine])
def list_machines(db: Session = Depends(get_db)):
    print("Listando todas as máquinas", db.query(models.Machine).all())
    return db.query(models.Machine).all()

# Apagar uma máquina
@app.delete("/machines/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    try:        
        db_machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
        if db_machine is None:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        # Chama o serviço de remoção da máquina
        response_service = remover_maquina(str(db_machine.model_id))
        if "error" in response_service:
            raise HTTPException(status_code=400, detail=f"Erro ao remover a máquina: {response_service['error']}")
        
        db.delete(db_machine)
        db.commit()
        return {"status": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao remover a máquina: {str(e)}")

# Iniciar o treinamento de um modelo
@app.post("/train/")
def train_model(file: UploadFile, machine_id: int, target_column: str, db: Session = Depends(get_db)):
    print("Iniciando o treinamento para a máquina ID:", machine_id)
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    try:
        db_machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
        if db_machine is None:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        response_service = treinar_modelo(file, db_machine.model_id, target_column)
        if "error" in response_service:
            raise HTTPException(status_code=400, detail=f"Erro ao treinar a máquina: {response_service['error']}")
        return {"message": "Training started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao treinar a máquina: {str(e)}")
    
# Resposta do treinamento
@app.post("/webhook/treinamento/")
async def webhook_treinamento(request: Request, db: Session = Depends(get_db)):
    try:
        # Extrai os dados do corpo da requisição
        data = await request.json()
        print("Dados recebidos via Webhook:", data)

        # Verifica se os dados necessários estão presentes
        model_id = data.get("model_id")
        status = data.get("status")
        metrics = data.get("metrics")


        if not model_id or not status:
            print(f"Erro: Dados incompletos. Model ID: {model_id}, Status: {status}")
            raise HTTPException(status_code=400, detail="Dados incompletos enviados pelo webhook")

        # Atualiza o status do modelo no banco (tabela "machines")
        db_machine = db.query(models.Machine).filter(models.Machine.model_id == model_id).first()
        if not db_machine:
            print(f"Erro: Máquina com ID {model_id} não encontrada no banco.")
            raise HTTPException(status_code=404, detail="Máquina não encontrada")
        
        db_machine.status = status
        if metrics:
            db_machine.metrics = metrics  # Atualiza as métricas, se existirem

        db.commit()

        return {"message": "Status do modelo atualizado com sucesso", "model_id": model_id, "status": status}

    except Exception as e:
        print(f"Erro ao processar o webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar o webhook: {str(e)}")

# Busca ranking
@app.get("/ranking/")
def get_ranking(machine_id: int = None, db: Session = Depends(get_db)):
    print("Obtendo ranking para a máquina ID:", machine_id)
    db_machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    print("Máquina encontrada no banco:", db_machine.model_id)
    if not db_machine:
        raise HTTPException(status_code=404, detail="Maquina não encontrado")
    
    try:
        ranking = obter_ranking(db_machine.model_id)
        return {"ranking": ranking, "metrics": db_machine.metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter o ranking: {str(e)}")