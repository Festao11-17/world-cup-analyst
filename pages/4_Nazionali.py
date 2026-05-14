import os
import streamlit as st
import pandas as pd

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Brasile":      "Girone_C/Brasile",
    "Francia":      "Girone_I/Francia",
    "Argentina":    "Girone_J/Argentina",
    "Inghilterra":  "Girone_L/Inghilterra",
    "Spagna":       "Girone_H/Spagna",
    "Portogallo":   "Girone_K/Portogallo",
    "Germania":     "Girone_E/Germania",
    "Olanda":       "Girone_F/Olanda",
    "Belgio":       "Girone_G/Belgio",
    "Croazia":      "Girone_L/Croazia",
    "Uruguay":      "Girone_H/Uruguay",
    "Colombia":     "Girone_K/Colombia",
    "Marocco":      "Girone_C/Marocco",
    "Senegal":      "Girone_I/Senegal",
    "Giappone":     "Girone_F/Giappone",
    "Messico":      "Girone_A/Messico",
    "USA":          "Girone_D/Stati_Uniti",
    "Australia":    "Girone_D/Australia",
    "Norvegia":     "Girone_I/Norvegia",
    "Svizzera":     "Girone_B/Svizzera",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

st.markdown("<h1>🌍 NAZIONALI</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/world_cup_players.csv")

col1, col2, col3 = st.columns(3)
with col1:
    teams = ["Tutte"] + sorted(df["Squadra"].unique().tolist())
    selected_team = st.selectbox("Squadra", teams)
with col2:
    roles = ["Tutti"] + sorted(df["Ruolo"].unique().tolist())
    selected_role = st.selectbox("Ruolo", roles)
with col3:
    search = st.text_input("🔍 Cerca giocatore")

filtered = df.copy()
if selected_team != "Tutte":
    filtered = filtered[filtered["Squadra"] == selected_team]
if selected_role != "Tutti":
    filtered = filtered[filtered["Ruolo"] == selected_role]
if search:
    filtered = filtered[filtered["Giocatore"].str.contains(search, case=False)]

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
            f"</div></div>",
            unsafe_allow_html=True
        )