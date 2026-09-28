# 🏎️ OpenF1 Data Collector - MongoDB

Este projeto é um script em Python desenvolvido como atividade acadêmica do curso de Ciência da Computação no UNIPÊ. O objetivo principal é consumir dados da API REST pública da [OpenF1](https://openf1.org/) (incluindo informações sobre sessões de corrida, pilotos e voltas) e armazená-los de forma estruturada e idempotente em um banco de dados NoSQL MongoDB.
Faça o readmi desse projeto para que eu coloque no meu github
## ✨ Funcionalidades

* **Integração de API REST:** Consumo eficiente dos endpoints `/sessions`, `/drivers` e `/laps`.
* **Idempotência:** Prevenção de dados duplicados no banco utilizando chaves compostas únicas e a operação `update_one` com `upsert=True`.
* **Modularidade e Boas Práticas:** Código estruturado em funções com responsabilidades únicas e tratamento de exceções em requisições HTTP e conexões com o banco.
* **Segurança:** Uso de variáveis de ambiente para ocultar credenciais e strings de conexão, garantindo que dados sensíveis não sejam enviados ao repositório.

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **MongoDB** (Driver `pymongo`)
* **Requests** (Para chamadas HTTP)
* **Python-dotenv** (Gerenciamento de configurações)

## 🛠️ Como Instalar e Executar

### Pré-requisitos
* Python 3 instalado na máquina.
* Servidor MongoDB rodando localmente (porta 27017) ou uma conta configurada no MongoDB Atlas.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/VictorsLima7/MongoDB-APIRest-Open-F1.git](https://github.com/VictorsLima7/MongoDB-APIRest-Open-F1.git)
   cd MongoDB-APIRest-Open-F1

   Instale as dependências
   python -m pip install -r requirements.txt

   Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto e adicione a sua string de conexão do MongoDB:
MONGO_URI=mongodb://localhost:27017/

Execute o script principal:
python f1_data_collector.py

📂 Estrutura do Banco de Dados

O script cria ou utiliza o banco de dados chamado openf1_data com três collections principais, cada uma protegida contra duplicatas por chaves únicas:

    sessions: Armazena os dados das sessões de corrida (Chave única: session_key).

    drivers: Armazena os dados dos pilotos que participaram de uma sessão (Chaves únicas: session_key + driver_number).

    laps: Armazena os dados de telemetria e o histórico das voltas (Chaves únicas: session_key + driver_number + lap_number).

