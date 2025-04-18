# Google Ads MCP API

API para gerenciamento e monitoramento de contas do Google Ads através de uma interface RESTful.

## Funcionalidades

- Listar contas de cliente
- Listar campanhas por conta
- Obter métricas de desempenho de campanhas
- Atualizar orçamentos e lances de campanhas

## Estrutura do Projeto

- `app/` - Código principal da aplicação
  - `routers/` - Rotas da API
  - `services/` - Serviços para interação com a API do Google Ads
- `.env` - Arquivo de configuração com variáveis de ambiente
- `Dockerfile` - Configuração para criação da imagem Docker
- `requirements.txt` - Dependências Python

## Configuração

Para configurar a API, crie um arquivo `.env` com as seguintes variáveis:

```
# Server Configuration
HOST=0.0.0.0
PORT=8080
LOG_LEVEL=INFO
DEBUG=False

# Google Ads API Configuration
GOOGLE_ADS_DEVELOPER_TOKEN=seu_developer_token
GOOGLE_ADS_CLIENT_ID=seu_client_id
GOOGLE_ADS_CLIENT_SECRET=seu_client_secret
GOOGLE_ADS_REFRESH_TOKEN=seu_refresh_token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=seu_login_customer_id
```

## Instalação e Execução

### Usando Docker (recomendado)

1. Construa a imagem Docker:
   ```
   docker build -t google-ads-mcp-api:latest .
   ```

2. Execute o container:
   ```
   docker run -d -p 8081:8080 --name google-ads-mcp-api google-ads-mcp-api:latest
   ```

### Execução Local

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Execute a aplicação:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8080
   ```

## Endpoints da API

### Listar Contas de Cliente

```
GET /api/google-ads/accounts
```

### Listar Campanhas

```
GET /api/google-ads/campaigns/{customer_id}
```

Parâmetros opcionais:
- `status`: Filtrar por status (ENABLED, PAUSED, REMOVED)

### Métricas de Desempenho

```
GET /api/google-ads/performance/{customer_id}
```

Parâmetros opcionais:
- `campaign_ids`: Lista de IDs de campanhas separados por vírgula
- `date_range`: Período do relatório (LAST_7_DAYS, LAST_30_DAYS)

### Atualizar Orçamento/Lance

```
POST /api/google-ads/update-bid-budget
```

Corpo da requisição:
```json
{
  "customerId": "123456789",
  "campaignId": "987654321",
  "newBudget": 100.0,
  "newBid": 1.2
}
```

## Documentação

A documentação completa da API está disponível em:

```
http://seu-servidor:porta/docs
``` 