import streamlit as st
import pandas as pd

st.title("🕵️ Player Scouting")

# DATI
df = pd.read_csv("data/world_cup_players.csv")

# FILTRI
roles = ["Tutti"] + sorted(df["Ruolo"].unique().tolist())

selected_role = st.selectbox(
    "Ruolo",
    roles
)

search_player = st.text_input(
    "Cerca Giocatore"
)

max_age = st.slider(
    "Età Massima",
    18,
    40,
    25
)

# FILTER
filtered_df = df.copy()

if selected_role != "Tutti":
    filtered_df = filtered_df[
        filtered_df["Ruolo"] == selected_role
    ]

filtered_df = filtered_df[
    filtered_df["Età"] <= max_age
]

if search_player:
    filtered_df = filtered_df[
        filtered_df["Giocatore"].str.contains(
            search_player,
            case=False
        )
    ]

# SORT
filtered_df = filtered_df.sort_values(
    by="xG",
    ascending=False
)

st.markdown("---")

# PLAYERS
for _, row in filtered_df.iterrows():

    player_image = f"assets/players/{row['Giocatore'].lower()}.png"

    col1, col2 = st.columns([1, 5])

    with col1:
        st.image(player_image, width=90)

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

        🌍 {row['Squadra']} <br>
        ⚽ {row['Ruolo']} <br>
        🎂 {row['Età']} anni <br>
        📈 xG: {row['xG']} <br>
        🥅 Gol: {row['Gol']} <br>
        🎯 Assist: {row['Assist']}

        </div>
        """, unsafe_allow_html=True)