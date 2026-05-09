import streamlit as st
import pandas as pd
import random

st.title("🔮 Predizione Partite")

# CARICAMENTO DATI
df = pd.read_csv("data/team_stats.csv")

teams = df["Squadra"].tolist()

# SELEZIONE SQUADRE
team1 = st.selectbox("Seleziona Squadra Casa", teams)
team2 = st.selectbox("Seleziona Squadra Ospite", teams, index=1)

st.markdown("---")

# DATI
team1_data = df[df["Squadra"] == team1].iloc[0]
team2_data = df[df["Squadra"] == team2].iloc[0]

# CALCOLO SEMPLICE PREDIZIONE
team1_strength = (
    team1_data["Gol"] +
    team1_data["xG"] +
    team1_data["Possesso"] / 20
)

team2_strength = (
    team2_data["Gol"] +
    team2_data["xG"] +
    team2_data["Possesso"] / 20
)

total = team1_strength + team2_strength

team1_probability = round((team1_strength / total) * 100)
team2_probability = round((team2_strength / total) * 100)

# SCORE PREDICTION
team1_goals = random.randint(0, 3)
team2_goals = random.randint(0, 3)

# UI
col1, col2 = st.columns(2)

with col1:
    st.subheader(team1)
    st.metric("Probabilità Vittoria", f"{team1_probability}%")

with col2:
    st.subheader(team2)
    st.metric("Probabilità Vittoria", f"{team2_probability}%")

st.markdown("---")

st.subheader("⚽ Risultato Previsto")

st.markdown(f"""
# {team1_goals} - {team2_goals}
### {team1} vs {team2}
""")

st.markdown("---")

# ANALISI
if team1_probability > team2_probability:
    st.success(f"{team1} parte favorita secondo i dati.")
elif team2_probability > team1_probability:
    st.success(f"{team2} parte favorita secondo i dati.")
else:
    st.info("Partita molto equilibrata.")