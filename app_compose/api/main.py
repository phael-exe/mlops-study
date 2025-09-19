import redis
import os
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI(
    title="API Contadora",
    description="API simples que usa Redis para contar visitas",
    version="1.0.0",
)

load_dotenv()
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

db = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

db.setnx('hits', 0)

@app.get("/")
def boas_vindas():
    return {"mensagem": "Aplicaçdehhuide está rodando 🚀"}

@app.get("/visits")
def visits_count():
    
    visits = db.incr('hits')
    return {"total_visits": visits}