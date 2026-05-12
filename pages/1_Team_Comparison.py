import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

FLAG_MAP = {
    "Brasile":      "Girone_C/brasile",
    "Francia":      "Girone_I/francia",
    "Argentina":    "Girone_J/argentina",
    "Inghilterra":  "Girone_L/inghilterra",
    "Spagna":       "Girone_H/spagna",
    "Portogallo":   "Girone_K/portogallo",
    "Germania":     "Girone_E/germania",
    "Olanda":       "Girone_F/olanda",
    "Belgio":       "Girone_G/belgio",
    "Croazia":      "Girone_L/croazia",
    "Uruguay":      "Girone_H/uruguay",
    "Colombia":     "Girone_K/colombia",
    "Marocco":      "Girone_C/marocco",
    "Senegal":      "Girone_I/senegal",
    "Giappone":     "Girone_F/giappone",
    "Messico":      "Girone_A/messico",
    "USA":          "Girone_D/stati_uniti",
    "Australia":    "Girone_D/australia",
    "Norvegia":     "Girone_I/norvegia",
    "Svizzera":     "Girone_B/svizzera",
}
def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s.lower())}.png"

st.markdown("<h1>📊 TEAM COMPARISON</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
teams = df["Squadra"].tolist()

col1, col2 = st.columns(2)
with col1: team1 = st.selectbox("Squadra 1", teams, index=0)
with col2: team2 = st.selectbox("Squadra 2", teams, index=1)

t1 = df[df["Squadra"]==team1].iloc[0]
t2 = df[df["Squadra"]==team2].iloc[0]

st.markdown("---")

col_l, col_c, col_r = st.columns([3,1,3])
with col_l:
    fp = flag_path(team1)
    if os.path.exists(fp): st.image(fp, width=60)
    st.markdown(f"### {team1}")
    c1,c2,c3 = st.columns(3)
    c1.metric("Gol", t1["Gol"])
    c2.metric("xG", t1["xG"])
    c3.metric("Possesso", f"{t1['Possesso']}%")

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "</div>", unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(team2)
    if os.path.exists(fp2): st.image(fp2, width=60)
    st.markdown(f"### {team2}")
    c1,c2,c3 = st.columns(3)
    c1.metric("Gol", t2["Gol"])
    c2.metric("xG", t2["xG"])
    c3.metric("Possesso", f"{t2['Possesso']}%")

st.markdown("---")

stats = ["Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
fig = go.Figure()
for team, data, color in [(team1, t1, "#00d4ff"), (team2, t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[data[s] for s in stats], theta=stats,
        fill='toself', name=team, line=dict(color=color, width=2)
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(bgcolor="rgba(26,32,53,0.6)",
               radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"),
               angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=420, showlegend=True
)
st.markdown("<span class='wca-section-label'>📈 Confronto Radar</span>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)