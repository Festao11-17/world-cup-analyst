import streamlit as st

st.set_page_config(
    page_title="World Cup Analyst",
    page_icon="⚽",
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

# PAGINA PRINCIPALE
st.title("⚽ World Cup Analyst")

st.subheader("Piattaforma di analisi dati sul Mondiale 2026")

st.markdown("---")

# HERO SECTION
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Analizza il calcio come un vero data analyst.

    Confronta nazionali, esplora statistiche avanzate e scopri insight basati sui dati.
    """)

with col2:
    st.metric("Nazionali", "32")
    st.metric("Giocatori monitorati", "500+")

st.markdown("---")

# FEATURES
st.header("Funzionalità")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("📊 Confronto Squadre")
    st.write("Confronta le nazionali tramite metriche avanzate.")

with col2:
    st.info("👤 Confronto Giocatori")
    st.write("Analizza prestazioni e statistiche dei giocatori.")

with col3:
    st.warning("🔮 Predizioni Partite")
    st.write("Esplora previsioni basate sui dati.")

st.markdown("---")

st.caption("Realizzato con Python, Streamlit e dati calcistici.")