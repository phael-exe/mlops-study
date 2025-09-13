# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager
import uuid
import os

class QueryRequest(BaseModel):
    query: str

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Verificando e indexando documentos na inicialização (via lifespan)...")
    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print("Coleção já existe. Nenhum documento a ser indexado.")
    except Exception as e:
        print("Coleção não encontrada. Criando e indexando...")
        qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=embedding_model.get_sentence_embedding_dimension(),
                distance=models.Distance.COSINE
            )
        )
        with open("/app/data/test_doc.txt", "r") as f:
            documents = f.readlines()
        
        qdrant_client.upload_points(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding_model.encode(doc).tolist(),
                    payload={"text": doc.strip()}
                )
                for doc in documents if doc.strip()
            ]
        )
        print("Indexação concluída.")
    
    yield # <--- A API fica rodando a partir daqui

    # O código DEPOIS do 'yield' roda no encerramento (shutdown).
    print("API encerrada.")

# --- 3. PASSAMOS A FUNÇÃO LIFESPAN PARA O FASTAPI ---
app = FastAPI(
    title="API de Busca RAG",
    description="Uma API para buscar informações em documentos via busca vetorial.",
    lifespan=lifespan # <--- AQUI ESTÁ A MUDANÇA
)

# O endpoint continua exatamente o mesmo
@app.post("/ask", summary="Faz uma busca vetorial")
def ask_question(request: QueryRequest):
    """
    Recebe uma query, a transforma em vetor e busca os documentos mais
    relevantes no Qdrant.
    """
    try:
        query_vector = embedding_model.encode(request.query).tolist()

        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
        
        relevant_docs = [hit.payload['text'] for hit in search_result]

        return {
            "query": request.query,
            "relevant_documents": relevant_docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))