# ETL Cartola FC - Integração com MongoDB

Este projeto consiste em um script de ETL (Extração, Transformação e Carga) desenvolvido em Python para coletar dados da API não oficial do Cartola FC e armazená-los de forma estruturada em um banco de dados MongoDB. 

O sistema busca dados sobre o status do mercado, informações dos clubes e estatísticas dos atletas, organizando-os em coleções distintas. O objetivo é criar um repositório de dados robusto para futuras análises e criação de modelos preditivos.

## 🚀 Tecnologias Utilizadas

* **Python 3.9+**
* **MongoDB** (Local ou Atlas)
* Bibliotecas: `requests`, `pymongo`, `python-dotenv`

## ⚙️ Estrutura do Banco de Dados

Os dados são armazenados no banco `cartola_fc_db`, divididos nas seguintes coleções:
* `mercado_rodada_atual`: Metadados e status de abertura/fechamento do mercado.
* `clubes_rodada_atual`: Informações, escudos e abreviações dos times (utilizando operações de `upsert` para evitar duplicatas).
* `atletas_rodada_atual`: Lista completa de jogadores contendo preços, variações, pontuações, scouts e status de probabilidade.

Todos os registros recebem um campo `timestamp_coleta` no padrão ISO 8601 para rastreamento histórico.

## 🛠️ Como executar o projeto

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
   cd NOME_DO_REPOSITORIO

   Crie e ative um ambiente virtual:
   python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

Instale as dependências:

pip install requests pymongo python-dotenv


Configure o banco de dados:
Crie um arquivo chamado .env na raiz do projeto e insira a URI de conexão do seu MongoDB. Para rodar com um banco local, utilize:
MONGODB_URI=mongodb://localhost:27017/

Execute o pipeline de extração:
python cartola_etl.py
