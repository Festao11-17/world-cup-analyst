import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

st.markdown("<h1>🌟 PLAYER PROFILE</h1>", unsafe_allow_html=True)

df = pd.read_csv("data/world_cup_players.csv")
df_teams = pd.read_csv("data/team_stats.csv")

selected = st.selectbox("Seleziona Giocatore", df["Giocatore"].tolist())
player = df[df["Giocatore"] == selected].iloc[0]

st.markdown("---")

# HEADER
col_flag, col_info = st.columns([1, 5])
with col_flag:
    fp = flag_path(player["Squadra"])
    if os.path.exists(fp):
        st.image(fp, width=100)
with col_info:
    st.markdown(f"<h1>{selected}</h1>", unsafe_allow_html=True)
    role_colors = {"ATT":"wca-badge-red","ALA":"wca-badge-red","CEN":"wca-badge","DIF":"wca-badge","POR":"wca-badge"}
    rc = role_colors.get(player["Ruolo"], "wca-badge")
    st.markdown(
        f"<span class='{rc}'>{player['Ruolo']}</span> "
        f"<span class='wca-badge' style='margin-left:8px'>{player['Squadra']}</span> "
        f"<span style='color:#6b7a99;margin-left:12px;font-size:13px'>{player['Età']} anni · {player['Presenze']} presenze</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# KPI
st.markdown("<span class='wca-section-label'>📊 Statistiche</span>", unsafe_allow_html=True)
c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("⚽ Gol",       int(player["Gol"]))
c2.metric("🎯 Assist",    int(player["Assist"]))
c3.metric("📐 xG",        player["xG"])
c4.metric("🎯 Tiri",      int(player["Tiri"]))
c5.metric("⚡ Velocità",  int(player["Velocita"]))
c6.metric("🔑 KeyPasses", int(player["KeyPasses"]))

st.markdown("---")

# RADAR vs ruolo
st.markdown("<span class='wca-section-label'>📈 Radar vs Media Ruolo</span>", unsafe_allow_html=True)
stats = ["Gol","Assist","xG","Tiri","Velocita","KeyPasses"]
same  = df[df["Ruolo"] == player["Ruolo"]]
avg_v = [same[s].mean() for s in stats]
pl_v  = [player[s] for s in stats]

fig = go.Figure()
for r, name, color in [(pl_v, selected, "#00d4ff"), (avg_v, f"Media {player['Ruolo']}", "#6b7a99")]:
    fig.add_trace(go.Scatterpolar(
        r=r, theta=stats, fill='toself', name=name,
        line=dict(color=color, width=2)
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(bgcolor="rgba(26,32,53,0.6)",
               radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99"),
               angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99")),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=420, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# CONFRONTO AUTOMATICO
st.markdown("<span class='wca-section-label'>⚔️ Confronto — Stesso Ruolo</span>", unsafe_allow_html=True)
rivals = df[(df["Ruolo"]==player["Ruolo"]) & (df["Giocatore"]!=selected)].sort_values("Gol", ascending=False).head(5)

if not rivals.empty:
    compare = pd.concat([pd.DataFrame([player]), rivals]).reset_index(drop=True)
    colors  = ["#00d4ff" if g==selected else "#1f2d45" for g in compare["Giocatore"]]

    fig_bar = go.Figure(go.Bar(
        x=compare["Giocatore"], y=compare["Gol"],
        marker_color=colors, text=compare["Gol"], textposition="outside",
        marker_line_color="#1f2d45", marker_line_width=1
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8edf5"), height=320,
        xaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
        yaxis=dict(gridcolor="#1f2d45", color="#6b7a99"),
        margin=dict(t=20,b=20), showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# NAZIONALE
st.markdown(f"<span class='wca-section-label'>🏳️ Nazionale — {player['Squadra']}</span>", unsafe_allow_html=True)
team_row = df_teams[df_teams["Squadra"]==player["Squadra"]]
if not team_row.empty:
    t = team_row.iloc[0]
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Gol/Match", t["Gol"])
    c2.metric("xG",        t["xG"])
    c3.metric("Tiri",      t["Tiri"])
    c4.metric("Possesso",  f"{t['Possesso']}%")
    c5.metric("Precisione",f"{t['PrecisionePassaggi']}%")

teammates = df[(df["Squadra"]==player["Squadra"]) & (df["Giocatore"]!=selected)].sort_values("Gol", ascending=False)
if not teammates.empty:
    st.markdown("<span class='wca-section-label' style='margin-top:16px;display:block'>👥 Compagni</span>", unsafe_allow_html=True)
    st.dataframe(
        teammates[["Giocatore","Ruolo","Età","Gol","Assist","xG","Velocita"]].reset_index(drop=True),
        use_container_width=True, hide_index=True
    )