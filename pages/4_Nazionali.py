import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nazionali · World Cup Analyst",
    page_icon="assets/logo.png",   # ← favicon aggiornata
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FLAG_MAP COMPLETO — 48 SQUADRE FIFA WORLD CUP 2026
# ══════════════════════════════════════════════════════════════════
FLAG_MAP = {
    # Girone A
    "Cechia":           "Girone_A/Cechia",
    "Corea del Sud":    "Girone_A/Corea_del_Sud",
    "Messico":          "Girone_A/Messico",
    "Sudafrica":        "Girone_A/Sudafrica",
    # Girone B
    "Bosnia":           "Girone_B/Bosnia_ed_Erzegovina",
    "Canada":           "Girone_B/Canada",
    "Qatar":            "Girone_B/Qatar",
    "Svizzera":         "Girone_B/Svizzera",
    # Girone C
    "Brasile":          "Girone_C/Brasile",
    "Haiti":            "Girone_C/Haiti",
    "Marocco":          "Girone_C/Marocco",
    "Scozia":           "Girone_C/Scozia",
    # Girone D
    "Australia":        "Girone_D/Australia",
    "Paraguay":         "Girone_D/Paraguay",
    "USA":              "Girone_D/Stati_Uniti",
    "Turchia":          "Girone_D/Turchia",
    # Girone E
    "Costa d'Avorio":   "Girone_E/Costa_d'Avorio",
    "Curacao":          "Girone_E/Curacao",
    "Ecuador":          "Girone_E/Ecuador",
    "Germania":         "Girone_E/Germania",
    # Girone F
    "Giappone":         "Girone_F/Giappone",
    "Olanda":           "Girone_F/Olanda",
    "Svezia":           "Girone_F/Svezia",
    "Tunisia":          "Girone_F/Tunisia",
    # Girone G
    "Belgio":           "Girone_G/Belgio",
    "Egitto":           "Girone_G/Egitto",
    "Iran":             "Girone_G/Iran",
    "Nuova Zelanda":    "Girone_G/Nuova_Zelanda",
    # Girone H
    "Arabia Saudita":   "Girone_H/Arabia_Saudita",
    "Capo Verde":       "Girone_H/Capo_Verde",
    "Spagna":           "Girone_H/Spagna",
    "Uruguay":          "Girone_H/Uruguay",
    # Girone I
    "Francia":          "Girone_I/Francia",
    "Iraq":             "Girone_I/Iraq",
    "Norvegia":         "Girone_I/Norvegia",
    "Senegal":          "Girone_I/Senegal",
    # Girone J
    "Algeria":          "Girone_J/Algeria",
    "Argentina":        "Girone_J/Argentina",
    "Austria":          "Girone_J/Austria",
    "Giordania":        "Girone_J/Giordania",
    # Girone K
    "Colombia":         "Girone_K/Colombia",
    "Portogallo":       "Girone_K/Portogallo",
    "Rep. del Congo":   "Girone_K/Repubblica_del_Congo",
    "Uzbekistan":       "Girone_K/Uzbekistan",
    # Girone L
    "Croazia":          "Girone_L/Croazia",
    "Ghana":            "Girone_L/Ghana",
    "Inghilterra":      "Girone_L/Inghilterra",
    "Panama":           "Girone_L/Panama",
}

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=100)
    st.markdown("### WORLD CUP\nANALYST")
    st.markdown("---")
    st.markdown(
        "<span class='wca-badge'>FIFA WORLD CUP 2026</span>",
        unsafe_allow_html=True
    )

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("<h1>🌍 NAZIONALI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#6b7a99;margin-top:-8px;margin-bottom:16px'>"
    "48 nazionali qualificate · FIFA World Cup 2026</p>",
    unsafe_allow_html=True
)

df = pd.read_csv("data/world_cup_players.csv")

# ── FILTRI ────────────────────────────────────────────────────────────────────
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

# ── LISTA GIOCATORI ───────────────────────────────────────────────────────────
for _, row in filtered.iterrows():
    fp = flag_path(row["Squadra"])
    col_flag, col_card = st.columns([1, 8])
    with col_flag:
        if os.path.exists(fp):
            st.image(fp, width=40)
    with col_card:
        role_colors = {
            "ATT": "wca-badge-red", "ALA": "wca-badge-red",
            "CEN": "wca-badge",     "DIF": "wca-badge",
            "POR": "wca-badge"
        }
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