import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="World Cup Analyst",
    page_icon="assets/logo.png",
    layout="wide"
)

load_css()

# CARICAMENTO DATI
df_teams = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("⚽ World Cup Analyst")
st.sidebar.markdown("Analizza squadre, confronta giocatori ed esplora statistiche calcistiche.")
st.sidebar.markdown("---")
st.sidebar.info("🚀 Piattaforma analytics Mondiale 2026")

# HERO
st.title("⚽ World Cup Analyst")
st.markdown("### La piattaforma di analytics sul Mondiale 2026")
st.markdown("Analizza squadre, confronta giocatori ed esplora statistiche avanzate basate sui dati.")

st.markdown("---")

# ── TOP STATS ──────────────────────────────────────────────────────────────
st.subheader("📊 Top Stats")

best_attack = df_teams.loc[df_teams["Gol"].idxmax()]
best_xg     = df_teams.loc[df_teams["xG"].idxmax()]
best_poss   = df_teams.loc[df_teams["Possesso"].idxmax()]
top_scorer  = df_players.loc[df_players["Gol"].idxmax()]
top_assist  = df_players.loc[df_players["Assist"].idxmax()]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Miglior Attacco",   best_attack["Squadra"], f"{best_attack['Gol']} gol/partita")
c2.metric("📐 Miglior xG",        best_xg["Squadra"],     f"xG {best_xg['xG']}")
c3.metric("🔵 Miglior Possesso",  best_poss["Squadra"],   f"{best_poss['Possesso']}%")
c4.metric("🥇 Capocannoniere",    top_scorer["Giocatore"], f"{int(top_scorer['Gol'])} gol")
c5.metric("🎯 Top Assistman",     top_assist["Giocatore"], f"{int(top_assist['Assist'])} assist")

st.markdown("---")

# ── FEATURED MATCH ─────────────────────────────────────────────────────────
st.subheader("🔥 Featured Match")

# Confronto tra le prime due squadre per gol (partita più attesa)
top2 = df_teams.nlargest(2, "Gol")
t1 = top2.iloc[0]
t2 = top2.iloc[1]

col_left, col_center, col_right = st.columns([2, 1, 2])

with col_left:
    st.markdown(f"### 🏳️ {t1['Squadra']}")
    st.metric("Gol/Partita", t1["Gol"])
    st.metric("xG", t1["xG"])
    st.metric("Possesso", f"{t1['Possesso']}%")

with col_center:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## VS", unsafe_allow_html=False)

with col_right:
    st.markdown(f"### 🏳️ {t2['Squadra']}")
    st.metric("Gol/Partita", t2["Gol"])
    st.metric("xG", t2["xG"])
    st.metric("Possesso", f"{t2['Possesso']}%")

# Mini radar del featured match
stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[t1[s] for s in stats], theta=stats,
    fill='toself', name=t1["Squadra"], line_color='#1f77b4'
))
fig.add_trace(go.Scatterpolar(
    r=[t2[s] for s in stats], theta=stats,
    fill='toself', name=t2["Squadra"], line_color='#ff7f0e'
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=380,
    margin=dict(t=30, b=30)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── LEADERBOARD ────────────────────────────────────────────────────────────
st.subheader("🏆 Leaderboard Nazionali")

col_lb, col_pl = st.columns(2)

with col_lb:
    st.markdown("#### Ranking per Gol")
    df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
    df_ranked.index += 1
    df_ranked.index.name = "Pos"

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, row in df_ranked.iterrows():
        medal = medals.get(i, f"{i}.")
        st.markdown(
            f"{medal} **{row['Squadra']}** — "
            f"{row['Gol']} gol &nbsp;|&nbsp; xG {row['xG']} &nbsp;|&nbsp; Possesso {row['Possesso']}%",
            unsafe_allow_html=True
        )

with col_pl:
    st.markdown("#### Top Marcatori")
    top_scorers = df_players.sort_values("Gol", ascending=False).head(8).reset_index(drop=True)
    top_scorers.index += 1
    top_scorers.index.name = "Pos"

    for i, row in top_scorers.iterrows():
        medal = medals.get(i, f"{i}.")
        st.markdown(
            f"{medal} **{row['Giocatore']}** ({row['Squadra']}) — "
            f"{int(row['Gol'])} gol &nbsp;|&nbsp; {int(row['Assist'])} assist",
            unsafe_allow_html=True
        )

st.markdown("---")

# FEATURES
st.header("Funzionalità Principali")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 🌍 Nazionali\nStatistiche complete per ogni nazionale.")
with col2:
    st.markdown("### 📊 Confronto Squadre\nAnalizza e confronta le nazionali.")
with col3:
    st.markdown("### 👤 Confronto Giocatori\nConfronta performance e metriche.")
with col4:
    st.markdown("### 🔮 Match Prediction\nPredizioni basate sui dati.")