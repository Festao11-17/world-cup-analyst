import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("👤 Confronto Giocatori")

# CARICAMENTO DATI
df = pd.read_csv("data/world_cup_players.csv")

# LISTA GIOCATORI
players = df["Giocatore"].tolist()

# SELECTBOX
player1 = st.selectbox("Seleziona Giocatore 1", players)
player2 = st.selectbox("Seleziona Giocatore 2", players, index=1)

# DATI GIOCATORI
player1_data = df[df["Giocatore"] == player1].iloc[0]
player2_data = df[df["Giocatore"] == player2].iloc[0]

# IMMAGINI
player1_image = f"assets/players/{player1.lower()}.png"
player2_image = f"assets/players/{player2.lower()}.png"

st.markdown("---")

# METRICHE
col1, col2 = st.columns(2)

with col1:
    if os.path.exists(player1_image):
        st.image(player1_image, width=200)
    else:
        st.markdown("<div style='font-size:80px;text-align:center'>👤</div>", unsafe_allow_html=True)
    st.subheader(player1)
    st.caption(f"{player1_data['Squadra']} • {player1_data['Ruolo']} • {player1_data['Età']} anni")
    st.metric("Gol", player1_data["Gol"])
    st.metric("Assist", player1_data["Assist"])
    st.metric("xG", player1_data["xG"])

with col2:
    if os.path.exists(player2_image):
        st.image(player2_image, width=200)
    else:
        st.markdown("<div style='font-size:80px;text-align:center'>👤</div>", unsafe_allow_html=True)
    st.subheader(player2)
    st.caption(f"{player2_data['Squadra']} • {player2_data['Ruolo']} • {player2_data['Età']} anni")
    st.metric("Gol", player2_data["Gol"])
    st.metric("Assist", player2_data["Assist"])
    st.metric("xG", player2_data["xG"])

st.markdown("---")

# RADAR CHART
stats = ["Gol", "Assist", "xG", "Tiri", "Velocita"]

player1_values = [player1_data[stat] for stat in stats]
player2_values = [player2_data[stat] for stat in stats]

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
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.subheader("📈 Confronto Statistiche")
st.plotly_chart(fig, use_container_width=True)