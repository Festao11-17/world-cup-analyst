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

st.markdown("<h1>🏳️ TEAM PROFILE</h1>", unsafe_allow_html=True)

df_teams  = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
df_ranked["Ranking"] = df_ranked.index + 1

teams = df_ranked["Squadra"].tolist()
selected = st.selectbox("Seleziona Nazionale", teams)

team    = df_ranked[df_ranked["Squadra"] == selected].iloc[0]
players = df_players[df_players["Squadra"] == selected]

st.markdown("---")

# HEADER
col_flag, col_info = st.columns([1, 5])
with col_flag:
    fp = flag_path(selected)
    if os.path.exists(fp):
        st.image(fp, width=110)
    else:
        st.markdown("<div style='font-size:80px'>🏳️</div>", unsafe_allow_html=True)

with col_info:
    medals = {1:"🥇", 2:"🥈", 3:"🥉"}
    rank_lbl = medals.get(int(team["Ranking"]), f"#{int(team['Ranking'])}")
    max_g, min_g = df_teams["Gol"].max(), df_teams["Gol"].min()
    rating = int(((team["Gol"] - min_g) / (max_g - min_g)) * 30 + 65)
    st.markdown(f"<h1>{selected}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<span class='wca-badge'>{rank_lbl} Ranking</span> "
        f"<span class='wca-badge' style='margin-left:8px'>⭐ {rating}/100 Rating</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# TEAM STATS
st.markdown("<span class='wca-section-label'>📊 Team Stats</span>", unsafe_allow_html=True)
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("⚽ Gol/Match",  team["Gol"])
c2.metric("📐 xG",         team["xG"])
c3.metric("🔵 Possesso",   f"{team['Possesso']}%")
c4.metric("✅ Precisione", f"{team['PrecisionePassaggi']}%")
c5.metric("🎯 Tiri",       team["Tiri"])

st.markdown("---")

# RADAR
st.markdown("<span class='wca-section-label'>📈 Stile di Gioco</span>", unsafe_allow_html=True)
stats = ["Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
avg   = [df_teams[s].mean() for s in stats]
vals  = [team[s] for s in stats]

fig = go.Figure()
for r, name, color in [(vals, selected, "#00d4ff"), (avg, "Media Mondiale", "#6b7a99")]:
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
    height=400, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# TOP PLAYERS
if not players.empty:
    st.markdown("<span class='wca-section-label'>⭐ Top Players</span>", unsafe_allow_html=True)
    top_sc = players.loc[players["Gol"].idxmax()]
    top_as = players.loc[players["Assist"].idxmax()]
    youngest= players.loc[players["Età"].idxmin()]
    fastest = players.loc[players["Velocita"].idxmax()]

    for col, label, emoji, p in zip(
        st.columns(4),
        ["Miglior Marcatore","Miglior Assistman","Più Giovane","Più Veloce"],
        ["⚽","🎯","🌱","⚡"],
        [top_sc, top_as, youngest, fastest]
    ):
        with col:
            st.markdown(
                f"<div class='wca-card' style='text-align:center'>"
                f"<div style='font-size:2rem'>{emoji}</div>"
                f"<span class='wca-badge' style='margin:8px 0;display:inline-block'>{label}</span>"
                f"<div style='font-weight:700;font-size:15px;margin-top:8px'>{p['Giocatore']}</div>"
                f"<div style='color:#6b7a99;font-size:12px'>{p['Ruolo']} · {p['Età']} anni</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ROSA
    st.markdown("<span class='wca-section-label'>👥 Rosa Completa</span>", unsafe_allow_html=True)
    show_cols = ["Giocatore","Ruolo","Età","Presenze","Gol","Assist","xG","KeyPasses","Dribbling","Velocita"]
    st.dataframe(
        players[show_cols].sort_values("Gol", ascending=False).reset_index(drop=True),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # TEAM STRENGTH
    st.markdown("<span class='wca-section-label'>💪 Team Strength</span>", unsafe_allow_html=True)
    att = players[players["Ruolo"].isin(["ATT","ALA"])]
    mid = players[players["Ruolo"] == "CEN"]
    att_s = int(min(100, att["Gol"].mean()*3 + att["xG"].mean()*2)) if not att.empty else 50
    mid_s = int(min(100, mid["Assist"].mean()*4 + mid["Presenze"].mean()/2)) if not mid.empty else 50
    def_s = int((team["Possesso"]*0.6 + team["PrecisionePassaggi"]*0.4)*0.9)

    for label, score, color in [
        ("⚔️ Attacco",     att_s, "#ff3b5c"),
        ("🔄 Centrocampo", mid_s, "#00d4ff"),
        ("🛡️ Difesa",      def_s, "#00e5a0"),
    ]:
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
            f"<span style='font-size:13px;font-weight:600'>{label}</span>"
            f"<span style='color:#6b7a99;font-size:12px'>{score}/100</span></div>"
            f"<div class='wca-bar-wrap'>"
            f"<div class='wca-bar' style='width:{score}%;background:{color}'></div></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # PREDICTION
    st.markdown("<span class='wca-section-label'>🔮 Prediction Rating</span>", unsafe_allow_html=True)
    for col_n in ["Gol","xG","Possesso","PrecisionePassaggi"]:
        mn, mx = df_teams[col_n].min(), df_teams[col_n].max()
        df_teams[f"_n_{col_n}"] = (df_teams[col_n]-mn)/(mx-mn) if mx!=mn else 0
    pred_row = df_teams[df_teams["Squadra"]==selected].iloc[0]
    score = round(pred_row["_n_Gol"]*35 + pred_row["_n_xG"]*25 +
                  pred_row["_n_Possesso"]*20 + pred_row["_n_PrecisionePassaggi"]*20, 1)*100

    col_g, col_d = st.columns([1,2])
    with col_g:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            title={"text":"Win Score","font":{"color":"#6b7a99","size":13}},
            number={"font":{"color":"#e8edf5","size":40}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":"#6b7a99"},
                "bar":{"color":"#00d4ff"},
                "bgcolor":"rgba(0,0,0,0)",
                "bordercolor":"#1f2d45",
                "steps":[
                    {"range":[0,40],"color":"rgba(255,59,92,0.2)"},
                    {"range":[40,70],"color":"rgba(255,180,0,0.2)"},
                    {"range":[70,100],"color":"rgba(0,229,160,0.2)"},
                ]
            }
        ))
        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=260,
            font={"color":"#e8edf5"},
            margin=dict(t=40,b=10)
        )
        st.plotly_chart(gauge, use_container_width=True)

    with col_d:
        if score >= 70:
            badge, desc = "🟢 FAVORITA", "Statistiche superiori alla media. Alta probabilità di arrivare in fondo al torneo."
        elif score >= 45:
            badge, desc = "🟡 COMPETITIVA", "Nazionale solida con buone chance di superare i gironi e arrivare ai quarti."
        else:
            badge, desc = "🔴 OUTSIDER", "Statistiche sotto media. Può sorprendere, ma serve un salto di qualità."
        st.markdown(f"<br><span class='wca-badge'>{badge}</span>", unsafe_allow_html=True)
        st.markdown(f"<p style='margin-top:12px;color:#6b7a99'>{desc}</p>", unsafe_allow_html=True)
        st.markdown(f"**Score:** `{score}/100`")