import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Messico":"Girone_A/Messico","Cechia":"Girone_A/Cechia","Corea_del_Sud":"Girone_A/Corea_del_Sud","Sudafrica":"Girone_A/Sudafrica",
    "Svizzera":"Girone_B/Svizzera","Canada":"Girone_B/Canada","Bosnia_ed_Erzegovina":"Girone_B/Bosnia_ed_Erzegovina","Qatar":"Girone_B/Qatar",
    "Brasile":"Girone_C/Brasile","Marocco":"Girone_C/Marocco","Haiti":"Girone_C/Haiti","Scozia":"Girone_C/Scozia",
    "Australia":"Girone_D/Australia","Stati_Uniti":"Girone_D/Stati_Uniti","Paraguay":"Girone_D/Paraguay","Turchia":"Girone_D/Turchia",
    "Germania":"Girone_E/Germania","Ecuador":"Girone_E/Ecuador","Costa_d'Avorio":"Girone_E/Costa_d'Avorio","Curacao":"Girone_E/Curacao",
    "Giappone":"Girone_F/Giappone","Olanda":"Girone_F/Olanda","Svezia":"Girone_F/Svezia","Tunisia":"Girone_F/Tunisia",
    "Belgio":"Girone_G/Belgio","Egitto":"Girone_G/Egitto","Iran":"Girone_G/Iran","Nuova_Zelanda":"Girone_G/Nuova_Zelanda",
    "Spagna":"Girone_H/Spagna","Uruguay":"Girone_H/Uruguay","Arabia_Saudita":"Girone_H/Arabia_Saudita","Capo_Verde":"Girone_H/Capo_Verde",
    "Francia":"Girone_I/Francia","Senegal":"Girone_I/Senegal","Norvegia":"Girone_I/Norvegia","Iraq":"Girone_I/Iraq",
    "Argentina":"Girone_J/Argentina","Algeria":"Girone_J/Algeria","Austria":"Girone_J/Austria","Giordania":"Girone_J/Giordania",
    "Portogallo":"Girone_K/Portogallo","Colombia":"Girone_K/Colombia","Repubblica_del_Congo":"Girone_K/Repubblica_del_Congo","Uzbekistan":"Girone_K/Uzbekistan",
    "Inghilterra":"Girone_L/Inghilterra","Croazia":"Girone_L/Croazia","Ghana":"Girone_L/Ghana","Panama":"Girone_L/Panama",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"

st.markdown("<h1>👤 PLAYER COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/world_cup_players.csv")
players = sorted(df["Giocatore"].tolist())

# ── RICERCA ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    search1 = st.text_input("🔍 Cerca Giocatore 1", placeholder="Es. Messi...")
    filtered1 = [p for p in players if search1.lower() in p.lower()] if search1 else players
    p1 = st.selectbox("Giocatore 1", filtered1, key="p1")

with col2:
    search2 = st.text_input("🔍 Cerca Giocatore 2", placeholder="Es. Mbappe...")
    filtered2 = [p for p in players if search2.lower() in p.lower()] if search2 else players
    p2 = st.selectbox("Giocatore 2", filtered2, key="p2")

if p1 == p2:
    st.warning("Seleziona due giocatori diversi.")
    st.stop()

d1 = df[df["Giocatore"] == p1].iloc[0]
d2 = df[df["Giocatore"] == p2].iloc[0]

st.markdown("---")

# ── HEADER ───────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([3, 1, 3])

with col_l:
    fp = flag_path(d1["Squadra"])
    if os.path.exists(fp): st.image(fp, width=56)
    st.markdown(f"### {p1}")
    st.markdown(f"<span style='color:#6b7a99;font-size:12px'>{d1['Squadra']} · {d1['Ruolo']} · {d1['Età']} anni</span>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", int(d1["Gol"]))
    c2.metric("Assist", int(d1["Assist"]))
    c3.metric("xG", d1["xG"])

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "</div>", unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(d2["Squadra"])
    if os.path.exists(fp2): st.image(fp2, width=56)
    st.markdown(f"### {p2}")
    st.markdown(f"<span style='color:#6b7a99;font-size:12px'>{d2['Squadra']} · {d2['Ruolo']} · {d2['Età']} anni</span>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Gol", int(d2["Gol"]))
    c2.metric("Assist", int(d2["Assist"]))
    c3.metric("xG", d2["xG"])

st.markdown("---")

# ── STATS A CONFRONTO ────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Statistiche a Confronto</span>", unsafe_allow_html=True)

for label, k1, k2 in [
    ("⚽ Gol",        d1["Gol"],        d2["Gol"]),
    ("🎯 Assist",     d1["Assist"],     d2["Assist"]),
    ("📐 xG",         d1["xG"],         d2["xG"]),
    ("🎯 Tiri",       d1["Tiri"],       d2["Tiri"]),
    ("⚡ Velocità",   d1["Velocita"],   d2["Velocita"]),
    ("🔑 KeyPasses",  d1["KeyPasses"],  d2["KeyPasses"]),
    ("🎭 Dribbling",  d1["Dribbling"],  d2["Dribbling"]),
    ("📋 Presenze",   d1["Presenze"],   d2["Presenze"]),
]:
    max_v = max(float(k1), float(k2), 0.01)
    w1 = int(float(k1) / max_v * 100)
    w2 = int(float(k2) / max_v * 100)
    c1_col = "#00d4ff" if float(k1) >= float(k2) else "#6b7a99"
    c2_col = "#ff3b5c" if float(k2) > float(k1) else "#6b7a99"
    st.markdown(
        f"<div style='margin-bottom:12px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='font-weight:700;color:{c1_col}'>{k1}</span>"
        f"<span style='font-size:12px;color:#6b7a99'>{label}</span>"
        f"<span style='font-weight:700;color:{c2_col}'>{k2}</span>"
        f"</div>"
        f"<div style='display:flex;gap:4px'>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px;display:flex;justify-content:flex-end'>"
        f"<div style='width:{w1}%;background:#00d4ff;border-radius:4px;height:8px'></div></div>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px'>"
        f"<div style='width:{w2}%;background:#ff3b5c;border-radius:4px;height:8px'></div></div>"
        f"</div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── RADAR ────────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Radar</span>", unsafe_allow_html=True)

stats = ["Gol", "Assist", "xG", "Tiri", "Velocita", "KeyPasses", "Dribbling"]
fig = go.Figure()
for player, data, color in [(p1, d1, "#00d4ff"), (p2, d2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[data[s] for s in stats], theta=stats,
        fill='toself', name=player, line=dict(color=color, width=2)
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(bgcolor="rgba(26,32,53,0.6)",
               radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"),
               angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=440, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)