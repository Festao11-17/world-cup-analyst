import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title("🏳️ Team Profile")

# CARICAMENTO DATI
df_teams = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

# RANKING (basato su Gol)
df_teams_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
df_teams_ranked["Ranking"] = df_teams_ranked.index + 1

teams = df_teams_ranked["Squadra"].tolist()
selected_team = st.selectbox("Seleziona una Nazionale", teams)

team = df_teams_ranked[df_teams_ranked["Squadra"] == selected_team].iloc[0]
players = df_players[df_players["Squadra"] == selected_team]

st.markdown("---")

# ── HEADER ─────────────────────────────────────────────────────────────────
col_flag, col_info = st.columns([1, 4])

with col_flag:
    flag_image = f"assets/flags/{selected_team.lower()}.png"
    if os.path.exists(flag_image):
        st.image(flag_image, width=120)
    else:
        st.markdown("<div style='font-size:80px;text-align:center'>🏳️</div>", unsafe_allow_html=True)

with col_info:
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    rank_label = medals.get(int(team["Ranking"]), f"#{int(team['Ranking'])}")

    # Rating generale (0-100) basato su Gol normalizzati
    max_gol = df_teams["Gol"].max()
    min_gol = df_teams["Gol"].min()
    rating = int(((team["Gol"] - min_gol) / (max_gol - min_gol)) * 40 + 60)  # scala 60-100

    st.markdown(f"## {selected_team}")
    st.markdown(f"**Ranking:** {rank_label} &nbsp;&nbsp; **Rating Generale:** ⭐ {rating}/100")

st.markdown("---")

# ── TEAM STATS ─────────────────────────────────────────────────────────────
st.subheader("📊 Team Stats")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Gol/Partita",     team["Gol"])
c2.metric("📐 xG",              team["xG"])
c3.metric("🔵 Possesso",        f"{team['Possesso']}%")
c4.metric("✅ Prec. Passaggi",  f"{team['PrecisionePassaggi']}%")
c5.metric("🎯 Tiri",            team["Tiri"])

st.markdown("---")

# ── RADAR CHART ────────────────────────────────────────────────────────────
st.subheader("📈 Stile di Gioco — Radar")

stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
team_values = [team[s] for s in stats]
avg_values  = [df_teams[s].mean() for s in stats]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=team_values, theta=stats,
    fill='toself', name=selected_team, line_color='#1f77b4'
))
fig_radar.add_trace(go.Scatterpolar(
    r=avg_values, theta=stats,
    fill='toself', name='Media Mondiale',
    line_color='#aaa', opacity=0.5
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True, height=420
)
st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# ── TOP PLAYERS ────────────────────────────────────────────────────────────
st.subheader("⭐ Top Players")

if not players.empty:
    top_scorer  = players.loc[players["Gol"].idxmax()]
    top_assist  = players.loc[players["Assist"].idxmax()]
    youngest    = players.loc[players["Età"].idxmin()]
    fastest     = players.loc[players["Velocita"].idxmax()]

    c1, c2, c3, c4 = st.columns(4)

    def player_card(col, label, emoji, player_row):
        with col:
            img_path = f"assets/players/{player_row['Giocatore'].lower()}.png"
            if os.path.exists(img_path):
                st.image(img_path, width=100)
            else:
                st.markdown(f"<div style='font-size:50px;text-align:center'>{emoji}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="
                background-color:#1c1f26;
                padding:12px;
                border-radius:12px;
                border:1px solid #2d3748;
                text-align:center;
            ">
            <b>{label}</b><br>
            {player_row['Giocatore']}<br>
            <small>{player_row['Ruolo']} • {player_row['Età']} anni</small>
            </div>
            """, unsafe_allow_html=True)

    player_card(c1, "⚽ Miglior Marcatore", "⚽", top_scorer)
    player_card(c2, "🎯 Miglior Assistman", "🎯", top_assist)
    player_card(c3, "🌱 Più Giovane",       "🌱", youngest)
    player_card(c4, "⚡ Più Veloce",        "⚡", fastest)

    st.markdown("---")

    # Tabella completa rosa
    st.subheader("👥 Rosa Completa")
    st.dataframe(
        players[["Giocatore","Ruolo","Età","Presenze","Gol","Assist","xG","Velocita"]]
            .sort_values("Gol", ascending=False)
            .reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Nessun giocatore disponibile per questa nazionale.")

st.markdown("---")

# ── TEAM STRENGTH ──────────────────────────────────────────────────────────
st.subheader("💪 Team Strength")

if not players.empty:
    att_players = players[players["Ruolo"].isin(["ATT", "ALA"])]
    mid_players = players[players["Ruolo"] == "CEN"]

    # Attacco: media gol + xG degli attaccanti
    att_score = int(min(100, (att_players["Gol"].mean() * 3 + att_players["xG"].mean() * 2))) if not att_players.empty else 50
    # Centrocampo: media assist + presenze dei centrocampisti
    mid_score = int(min(100, (mid_players["Assist"].mean() * 4 + mid_players["Presenze"].mean() / 2))) if not mid_players.empty else 50
    # Difesa: stimata da possesso + precisione passaggi della squadra
    def_score = int((team["Possesso"] * 0.6 + team["PrecisionePassaggi"] * 0.4) * 0.9)

    def strength_bar(label, score, color):
        st.markdown(f"**{label}** &nbsp; `{score}/100`")
        bar_html = f"""
        <div style="background:#2d3748;border-radius:8px;height:22px;margin-bottom:14px;">
          <div style="width:{score}%;background:{color};height:22px;border-radius:8px;"></div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)

    strength_bar("⚔️ Attacco",      att_score, "#e74c3c")
    strength_bar("🔄 Centrocampo",  mid_score, "#3498db")
    strength_bar("🛡️ Difesa",       def_score, "#2ecc71")

st.markdown("---")

# ── PREDICTION RATING ──────────────────────────────────────────────────────
st.subheader("🔮 Prediction Rating")

if not players.empty:
    # Score composito
    norm_gol  = (team["Gol"]  - df_teams["Gol"].min())  / (df_teams["Gol"].max()  - df_teams["Gol"].min())
    norm_xg   = (team["xG"]   - df_teams["xG"].min())   / (df_teams["xG"].max()   - df_teams["xG"].min())
    norm_poss = (team["Possesso"] - df_teams["Possesso"].min()) / (df_teams["Possesso"].max() - df_teams["Possesso"].min())
    norm_pass = (team["PrecisionePassaggi"] - df_teams["PrecisionePassaggi"].min()) / (df_teams["PrecisionePassaggi"].max() - df_teams["PrecisionePassaggi"].min())

    prediction = round((norm_gol * 35 + norm_xg * 25 + norm_poss * 20 + norm_pass * 20) * 100, 1)

    col_pred, col_desc = st.columns([1, 2])

    with col_pred:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={"text": "Win Probability Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1f77b4"},
                "steps": [
                    {"range": [0,  40], "color": "#e74c3c"},
                    {"range": [40, 70], "color": "#f39c12"},
                    {"range": [70,100], "color": "#2ecc71"},
                ],
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_desc:
        if prediction >= 70:
            label = "🟢 Favorita"
            desc  = "Questa nazionale ha statistiche superiori alla media mondiale. Alta probabilità di arrivare in fondo al torneo."
        elif prediction >= 45:
            label = "🟡 Competitiva"
            desc  = "Nazionale solida con buone chance di passare i gironi e arrivare agli ottavi o quarti."
        else:
            label = "🔴 Outsider"
            desc  = "Statistiche sotto la media. Potrebbe sorprendere, ma dovrà migliorare per competere con le big."

        st.markdown(f"### {label}")
        st.markdown(desc)
        st.markdown(f"**Score:** `{prediction}/100`")