import requests
from fastapi import HTTPException, UploadFile

RELEVANCE_SERVICE_API_URL = "http://127.0.0.1:8000"  # URL da API do relevance-service

# função para cadastrar máquina no modelo
def cadastrar_maquina(nome_maquina: str):
    url = f"{RELEVANCE_SERVICE_API_URL}/models?model_name={nome_maquina}"
    try:
        response = requests.post(url)
        if response.status_code not in (200, 201):
            raise HTTPException(status_code=response.status_code, detail="Erro ao cadastrar a máquina.")
        print("retornou", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")

# função para remover máquina no modelo
def remover_maquina(model_id: str):
    url = f"{RELEVANCE_SERVICE_API_URL}/models/{model_id}"
    try:
        response = requests.delete(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erro ao remover a máquina.")
        print("retornou", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")
    
# função para treinar modelo na API relevance-service
def treinar_modelo(file: UploadFile, model_id: int, target_column: str):
    url = f"{RELEVANCE_SERVICE_API_URL}/train"
    
    file_bytes = file.file.read() 
    params = {'model_id': model_id, 'url': 'http://127.0.0.1:8001/webhook/treinamento/', "target_column": target_column}
    
    try:
        files = {'file': ('filename.csv', file_bytes, 'text/csv')}
        response = requests.post(url, files=files, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erro ao iniciar o treinamento do modelo.")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar conectar com o relevance-service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro de conexão com relevance-service: {str(e)}")

# função para obter ranking do modelo
def obter_ranking(model_id: int):
    url = f"{RELEVANCE_SERVICE_API_URL}/ranking?model_id={model_id}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erro ao obter o ranking do modelo.")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")