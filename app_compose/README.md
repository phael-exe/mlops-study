# Aplicação Contadora de Visitas com Docker Compose

Este é um projeto de exemplo que demonstra uma arquitetura de microsserviços usando Docker Compose.

A aplicação consiste em:
- **Frontend**: Uma aplicação Streamlit que exibe o contador de visitas.
- **Backend**: Uma API FastAPI que se comunica com o Redis para incrementar e retornar o número de visitas.
- **Banco de Dados**: Uma instância do Redis para persistir a contagem.

## Como executar

1.  **Crie o arquivo de ambiente:**
    Copie o arquivo `.env.template` para um novo arquivo chamado `.env` e preencha as variáveis:
    ```bash
    cp .env.template .env
    ```
    No arquivo `.env`, defina os seguintes valores:
    ```
    REDIS_HOST=redis
    REDIS_PORT=6379
    ```

2.  **Construa e suba os contêineres:**
    Execute o comando a seguir na raiz do projeto:
    ```bash
    docker-compose up --build
    ```

3.  **Acesse as aplicações:**
    *   **Frontend (Streamlit)**: [http://localhost:8501](http://localhost:8501)
    *   **API (FastAPI Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)
