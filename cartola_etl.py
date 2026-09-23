import os
import logging
import requests
from datetime import datetime, timezone
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

# Configuração de logs para indicar cada etapa do processo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def conectar_mongodb():
    """Lê as credenciais do ambiente e estabelece a conexão com o MongoDB."""
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        logging.error("Credenciais do MongoDB não encontradas no arquivo .env.")
        return None
        
    try:
        client = MongoClient(uri)
        # Retorna o objeto do banco de dados cartola_fc_db
        db = client.cartola_fc_db
        logging.info("Conectando ao MongoDB...")
        return db
    except Exception as e:
        logging.error(f"Erro ao conectar ao MongoDB: {e}")
        return None

def buscar_dados_mercado():
    """Faz uma requisição GET para a URL da API do Cartola FC e retorna o JSON."""
    url = "https://api.cartola.globo.com/atletas/mercado"
    
    try:
        logging.info("Buscando dados na API...")
        response = requests.get(url)
        # Tratamento de erros robusto verificando o status code
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar dados na API: {e}")
        return None

def processar_e_gravar_dados(db, dados_mercado):
    """Realiza a transformação e carga dos dados no MongoDB."""
    # Gera o timestamp no padrão ISO 8601
    timestamp_coleta = datetime.now(timezone.utc).isoformat()

    # 1. Dados dos Clubes
    if 'clubes' in dados_mercado:
        logging.info("Gravando dados dos clubes...")
        clubes_dict = dados_mercado['clubes']
        operacoes_clubes = []
        
        for clube_id_str, clube_info in clubes_dict.items():
            # Utiliza o id do clube como '_id' para facilitar o upsert
            clube_info['_id'] = int(clube_id_str) 
            operacoes_clubes.append(
                UpdateOne(
                    {'_id': clube_info['_id']}, 
                    {'$set': clube_info}, 
                    upsert=True
                )
            )
            
        if operacoes_clubes:
            db.clubes_rodada_atual.bulk_write(operacoes_clubes)

    # 2. Dados dos Atletas
    if 'atletas' in dados_mercado:
        logging.info("Gravando dados dos atletas...")
        atletas = dados_mercado['atletas']
        
        # Adiciona o campo timestamp_coleta a cada documento
        for atleta in atletas:
            atleta['timestamp_coleta'] = timestamp_coleta
            
        # Limpa a coleção para garantir apenas dados da última consulta
        db.atletas_rodada_atual.delete_many({}) 
        
        if atletas:
            # Insere a lista completa usando insert_many()
            db.atletas_rodada_atual.insert_many(atletas)

    # 3. Dados do Status do Mercado
    if 'status' in dados_mercado:
        logging.info("Gravando status do mercado...")
        status_mercado = dados_mercado['status']
        
        if isinstance(status_mercado, dict):
            status_mercado['timestamp_coleta'] = timestamp_coleta
            # Limpa a coleção antes de inserir para manter apenas o status mais recente
            db.mercado_rodada_atual.delete_many({})
            db.mercado_rodada_atual.insert_one(status_mercado)
        else:
             # Dependendo de como a API devolve o status, pode ser necessário formatar este bloco.
             # Para cobrir os dados gerais descritos, gravaremos os metadados diretamente se o formato for diferente
             db.mercado_rodada_atual.delete_many({})
             db.mercado_rodada_atual.insert_one({"status": status_mercado, "timestamp_coleta": timestamp_coleta})

if __name__ == "__main__":
    db = conectar_mongodb()
    
    if db is not None:
        dados = buscar_dados_mercado()
        
        if dados:
            processar_e_gravar_dados(db, dados)
            logging.info("Finalizado com sucesso.")
        else:
            logging.error("A execução foi interrompida pois não foi possível obter os dados da API.")
    else:
         logging.error("A execução foi interrompida pois a conexão com o MongoDB falhou.")