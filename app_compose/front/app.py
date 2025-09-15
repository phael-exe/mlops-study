import streamlit as st
import requests

st.set_page_config(layout="centered")

# URL da nossa API
API_URL = "http://api:8000/visits"

# --- Função para chamar a API ---
def get_visits_count():
    """Chama a API e retorna o número de visitas."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("total_visits", "Erro!")
    except requests.exceptions.RequestException:
        return "API Offline"

# --- Título ---
st.title("Contador de Visitas com Docker! 🐳")
st.markdown("---")
st.header("Contador em Tempo Real")

# --- Lógica com Session State (A CORREÇÃO DO BUG) ---

# 1. Se a contagem de visitas ainda não está na "memória" da sessão...
if 'visits' not in st.session_state:
    # ...busque o valor inicial da API e armazene-o.
    st.session_state.visits = get_visits_count()

# 2. O botão agora só precisa atualizar o valor na memória da sessão.
if st.button("Incrementar Visita 🔄"):
    st.session_state.visits = get_visits_count()
    st.success("Contador atualizado!")

# 3. Exibe o valor que está na memória da sessão.
# Este valor será sempre o mais atualizado.
st.metric(label="Total de Visitas no Redis", value=st.session_state.visits)