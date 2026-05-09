import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📊 Confronto Squadre")

# CARICAMENTO DATI
df = pd.read_csv("data/team_stats.csv")

# LISTA SQUADRE
teams = df["Squadra"].tolist()

# SELECTBOX
team1 = st.selectbox("Seleziona Squadra 1", teams)
team2 = st.selectbox("Seleziona Squadra 2", teams, index=1)

# DATI SQUADRE
team1_data = df[df["Squadra"] == team1].iloc[0]
team2_data = df[df["Squadra"] == team2].iloc[0]

st.markdown("---")

# METRICHE
col1, col2 = st.columns(2)

with col1:
    st.subheader(team1)
    st.metric("Gol", team1_data["Gol"])
    st.metric("xG", team1_data["xG"])
    st.metric("Possesso", f"{team1_data['Possesso']}%")

with col2:
    st.subheader(team2)
    st.metric("Gol", team2_data["Gol"])
    st.metric("xG", team2_data["xG"])
    st.metric("Possesso", f"{team2_data['Possesso']}%")

st.markdown("---")

# STATISTICHE
stats = [
    "Gol",
    "xG",
    "Tiri",
    "Possesso",
    "PrecisionePassaggi"
]

team1_values = [team1_data[stat] for stat in stats]
team2_values = [team2_data[stat] for stat in stats]

# RADAR CHART
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=team1_values,
    theta=stats,
    fill='toself',
    name=team1
))

fig.add_trace(go.Scatterpolar(
    r=team2_values,
    theta=stats,
    fill='toself',
    name=team2
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

st.subheader("📈 Confronto Statistiche")

st.plotly_chart(fig, use_container_width=True)