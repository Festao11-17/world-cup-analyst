import os
import streamlit as st
import pandas as pd

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Brasile":"Girone_C/brasile","Francia":"Girone_I/francia","Argentina":"Girone_J/argentina",
    "Inghilterra":"Girone_L/inghilterra","Spagna":"Girone_H/spagna","Portogallo":"Girone_K/portogallo",
    "Germania":"Girone_E/germania","Olanda":"Girone_F/olanda","Belgio":"Girone_G/belgio",
    "Croazia":"Girone_L/croazia","Uruguay":"Girone_H/uruguay","Colombia":"Girone_K/colombia",
    "Marocco":"Girone_C/marocco","Senegal":"Girone_I/senegal","Giappone":"Girone_F/giappone",
    "Messico":"Girone_A/messico","USA":"Girone_D/stati_uniti","Australia":"Girone_D/australia",
    "Norvegia":"Girone_I/norvegia","Svizzera":"Girone_B/svizzera",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s.lower())}.png"

st.markdown("<h1>🕵️ PLAYER SCOUTING</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/world_cup_players.csv")

col1, col2, col3 = st.columns(3)
with col1:
    roles = ["Tutti"] + sorted(df["Ruolo"].unique().tolist())
    selected_role = st.selectbox("Ruolo", roles)
with col2:
    search_player = st.text_input("🔍 Cerca Giocatore")
with col3:
    max_age = st.slider("Età Massima", 18, 40, 30)

# SORT
sort_by = st.selectbox("Ordina per", ["xG","Gol","Assist","Velocita","KeyPasses","Dribbling","PassAccuracy"])

# FILTER
filtered = df.copy()
if selected_role != "Tutti":
    filtered = filtered[filtered["Ruolo"] == selected_role]
filtered = filtered[filtered["Età"] <= max_age]
if search_player:
    filtered = filtered[filtered["Giocatore"].str.contains(search_player, case=False)]
filtered = filtered.sort_values(by=sort_by, ascending=False)

st.markdown("---")
st.markdown(
    f"<span class='wca-section-label'>{len(filtered)} giocatori trovati</span>",
    unsafe_allow_html=True
)

for _, row in filtered.iterrows():
    fp = flag_path(row["Squadra"])
    col_flag, col_card = st.columns([1, 8])

    with col_flag:
        if os.path.exists(fp):
            st.image(fp, width=40)

    with col_card:
        role_colors = {"ATT":"wca-badge-red","ALA":"wca-badge-red","CEN":"wca-badge","DIF":"wca-badge","POR":"wca-badge"}
        rc = role_colors.get(row["Ruolo"], "wca-badge")
        st.markdown(
            f"<div class='wca-card'>"
            f"<div style='display:flex;align-items:center;gap:12px;flex-wrap:wrap'>"
            f"<span style='font-weight:700;font-size:16px'>{row['Giocatore']}</span>"
            f"<span class='{rc}'>{row['Ruolo']}</span>"
            f"<span style='color:#6b7a99;font-size:12px'>{row['Squadra']} · {row['Età']} anni</span>"
            f"</div>"
            f"<div class='wca-stat-row'>"
            f"<div class='wca-stat'>⚽ Gol <span>{int(row['Gol'])}</span></div>"
            f"<div class='wca-stat'>🎯 Assist <span>{int(row['Assist'])}</span></div>"
            f"<div class='wca-stat'>📐 xG <span>{row['xG']}</span></div>"
            f"<div class='wca-stat'>⚡ Vel. <span>{int(row['Velocita'])}</span></div>"
            f"<div class='wca-stat'>🔑 Key <span>{int(row['KeyPasses'])}</span></div>"
            f"<div class='wca-stat'>🎭 Drib. <span>{row['Dribbling']}</span></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )