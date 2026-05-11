import streamlit as st
import pandas as pd

st.title("🌍 Nazionali")

# CARICAMENTO DATI
df = pd.read_csv("data/world_cup_players.csv")

# FILTRO SQUADRA
teams = ["Tutte"] + sorted(df["Squadra"].unique().tolist())

selected_team = st.selectbox(
    "Seleziona Squadra",
    teams
)

# FILTRO RUOLO
roles = ["Tutti"] + sorted(df["Ruolo"].unique().tolist())

selected_role = st.selectbox(
    "Seleziona Ruolo",
    roles
)

# SEARCH BAR
search_player = st.text_input("Cerca Giocatore")

# FILTRAGGIO
filtered_df = df.copy()

if selected_team != "Tutte":
    filtered_df = filtered_df[
        filtered_df["Squadra"] == selected_team
    ]

if selected_role != "Tutti":
    filtered_df = filtered_df[
        filtered_df["Ruolo"] == selected_role
    ]

if search_player:
    filtered_df = filtered_df[
        filtered_df["Giocatore"].str.contains(search_player, case=False)
    ]

st.markdown("---")

# TABELLA
for _, row in filtered_df.iterrows():
    flag_image = f"assets/flags/{row['Squadra'].lower()}.png"

    col1, col2 = st.columns([1, 5])

with col1:
    st.image(flag_image, width=60)

with col2:
    st.markdown(f"""
    <div style="
        background-color:#1c1f26;
        padding:20px;
        border-radius:15px;
        margin-bottom:15px;
        border:1px solid #2d3748;
    ">

    <h3>{row['Giocatore']}</h3>

    <p>
    🌍 {row['Squadra']} <br>
    ⚽ {row['Ruolo']} <br>
    🎂 {row['Età']} anni <br>
    🥅 Gol: {row['Gol']} <br>
    🎯 Assist: {row['Assist']}
    </p>

    </div>
    """, unsafe_allow_html=True)