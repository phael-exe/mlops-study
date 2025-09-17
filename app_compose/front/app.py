import streamlit as st
import requests

st.set_page_config(layout="centered")

API_URL = "http://api:8000/visits"

def get_visits_count():
    """Chama a API e retorna o número de visitas."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("total_visits", "Erro!")
    except requests.exceptions.RequestException:
        return "API Offline"

st.title("Contador de Visitas com Docker! 🐳")
st.markdown("---")
st.header("Contador em Tempo Real")

if 'visits' not in st.session_state:
    st.session_state.visits = get_visits_count()

if st.button("Incrementar Visita 🔄"):
    st.session_state.visits = get_visits_count()
    st.success("Contador atualizado!")

st.metric(label="Total de Visitas no Redis", value=st.session_state.visits)
