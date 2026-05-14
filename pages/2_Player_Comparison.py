import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

st.markdown("<h1>👤 PLAYER COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/world_cup_players.csv")
players = df["Giocatore"].tolist()

col1, col2 = st.columns(2)
with col1: p1 = st.selectbox("Giocatore 1", players, index=0)
with col2: p2 = st.selectbox("Giocatore 2", players, index=1)

d1 = df[df["Giocatore"]==p1].iloc[0]
d2 = df[df["Giocatore"]==p2].iloc[0]

st.markdown("---")

col_l, col_c, col_r = st.columns([3,1,3])
with col_l:
    fp = flag_path(d1["Squadra"])
    if os.path.exists(fp): st.image(fp, width=50)
    st.markdown(f"### {p1}")
    st.markdown(f"<span style='color:#6b7a99;font-size:12px'>{d1['Squadra']} · {d1['Ruolo']} · {d1['Età']} anni</span>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
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
    if os.path.exists(fp2): st.image(fp2, width=50)
    st.markdown(f"### {p2}")
    st.markdown(f"<span style='color:#6b7a99;font-size:12px'>{d2['Squadra']} · {d2['Ruolo']} · {d2['Età']} anni</span>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Gol", int(d2["Gol"]))
    c2.metric("Assist", int(d2["Assist"]))
    c3.metric("xG", d2["xG"])

st.markdown("---")

stats = ["Gol","Assist","xG","Tiri","Velocita","KeyPasses","Dribbling"]
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
st.markdown("<span class='wca-section-label'>📈 Confronto Radar</span>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)