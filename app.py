import streamlit as st

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.sidebar.image("assets/logo.png", width=120)

st.set_page_config(
    page_title="World Cup Analyst",
    page_icon="assets/logo.png",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("⚽ World Cup Analyst")

st.sidebar.markdown("""
Analizza squadre, confronta giocatori ed esplora statistiche calcistiche.
""")

st.sidebar.markdown("---")

st.sidebar.info("""
🚀 Piattaforma analytics Mondiale 2026
""")

# MAIN PAGE
st.title("⚽ World Cup Analyst")

st.markdown("""
## La piattaforma di analytics sul Mondiale 2026

Analizza squadre, confronta giocatori ed esplora statistiche avanzate basate sui dati.
""")

st.markdown("---")

# HERO
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 📊 Football Analytics Platform

    Confronta nazionali, scopri insight avanzati e utilizza predizioni basate sui dati per analizzare il Mondiale 2026.
    """)

    st.button("🚀 Inizia l'analisi")

with col2:
    st.metric("Nazionali", "32")
    st.metric("Giocatori", "500+")
    st.metric("Partite", "64")

st.markdown("---")

# FEATURES
st.header("Funzionalità Principali")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 Confronto Squadre

    Analizza e confronta le nazionali tramite statistiche avanzate.
    """)

with col2:
    st.markdown("""
    ### 👤 Confronto Giocatori

    Confronta performance e metriche dei migliori giocatori.
    """)

with col3:
    st.markdown("""
    ### 🔮 Match Prediction

    Esplora predizioni basate sui dati delle squadre.
    """)