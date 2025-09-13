# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY src/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/data ./data
COPY src/api .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]