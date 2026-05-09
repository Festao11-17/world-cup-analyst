import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("👤 Confronto Giocatori")

# CARICAMENTO DATI
df = pd.read_csv("data/player_stats.csv")

# LISTA GIOCATORI
players = df["Giocatore"].tolist()

# SELECTBOX
player1 = st.selectbox("Seleziona Giocatore 1", players)
player2 = st.selectbox("Seleziona Giocatore 2", players, index=1)

# DATI GIOCATORI
player1_data = df[df["Giocatore"] == player1].iloc[0]
player2_data = df[df["Giocatore"] == player2].iloc[0]
player1_image = f"assets/players/{player1.lower()}.png"
player2_image = f"assets/players/{player2.lower()}.png"

st.markdown("---")

# METRICHE
col1, col2 = st.columns(2)

with col1:
    st.image(player1_image, width=200)
    st.subheader(player1)
    st.metric("Gol", player1_data["Gol"])
    st.metric("Assist", player1_data["Assist"])
    st.metric("xG", player1_data["xG"])

with col2:
    st.image(player2_image, width=200)
    st.subheader(player2)
    st.metric("Gol", player2_data["Gol"])
    st.metric("Assist", player2_data["Assist"])
    st.metric("xG", player2_data["xG"])
    
st.markdown("---")

# STATISTICHE
stats = [
    "Gol",
    "Assist",
    "xG",
    "Tiri",
    "Velocita"
]

player1_values = [player1_data[stat] for stat in stats]
player2_values = [player2_data[stat] for stat in stats]

# RADAR CHART
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=player1_values,
    theta=stats,
    fill='toself',
    name=player1
))

fig.add_trace(go.Scatterpolar(
    r=player2_values,
    theta=stats,
    fill='toself',
    name=player2
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