import streamlit as st
import requests
import redis
import os

st.set_page_config(layout="centered")

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

def get_visits_count():
    """Chama a API e retorna o número de visitas."""
    try:
        db = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        visits = db.get("hits")
        return visits
    except requests.exceptions.RequestException:
        return "API Offline"

st.title("Contador de Mlops com Docker! 🐳")
st.markdown("---")
st.header("Contador em Tempo Real")

if 'visits' not in st.session_state:
    st.session_state.visits = get_visits_count()

st.metric(label="Total de Visitas no Redis", value=st.session_state.visits)
