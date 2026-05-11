import os
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

# TOP STATS PLAYER
best_scorer = df_players.loc[df_players["Gol"].idxmax()]
best_assist = df_players.loc[df_players["Assist"].idxmax()]
fastest_player = df_players.loc[df_players["Velocita"].idxmax()]

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

# TOP STATS
st.header("📈 Top Stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⚽ Miglior Marcatore",
        best_scorer["Giocatore"],
        f"{best_scorer['Gol']} gol"
    )

with col2:
    st.metric(
        "🎯 Più Assist",
        best_assist["Giocatore"],
        f"{best_assist['Assist']} assist"
    )

with col3:
    st.metric(
        "⚡ Più Veloce",
        fastest_player["Giocatore"],
        f"{fastest_player['Velocita']}"
    )

st.markdown("---")

# FEATURED MATCH
st.subheader("🔥 Featured Match")

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
    st.markdown("## VS")

with col_right:
    st.markdown(f"### 🏳️ {t2['Squadra']}")
    st.metric("Gol/Partita", t2["Gol"])
    st.metric("xG", t2["xG"])
    st.metric("Possesso", f"{t2['Possesso']}%")

# RADAR CHART
stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[t1[s] for s in stats], theta=stats,
    fill='toself', name=t1["Squadra"]
))
fig.add_trace(go.Scatterpolar(
    r=[t2[s] for s in stats], theta=stats,
    fill='toself', name=t2["Squadra"]
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=380
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# LEADERBOARD
st.subheader("🏆 Leaderboard Nazionali")

col_lb, col_pl = st.columns(2)

with col_lb:
    st.markdown("#### Ranking per Gol")
    df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
    df_ranked.index += 1

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for i, row in df_ranked.iterrows():
        medal = medals.get(i, f"{i}.")
        st.markdown(
            f"{medal} **{row['Squadra']}** — "
            f"{row['Gol']} gol | "
            f"xG {row['xG']} | "
            f"Possesso {row['Possesso']}%"
        )

with col_pl:
    st.markdown("#### Top Marcatori")
    top_scorers = df_players.sort_values("Gol", ascending=False).head(5)

    for _, row in top_scorers.iterrows():
        player_image = f"assets/players/{row['Giocatore'].lower()}.png"

        col1, col2 = st.columns([1, 4])

        with col1:
            if os.path.exists(player_image):
                st.image(player_image, width=80)
            else:
                st.markdown(
                    "<div style='font-size:48px;text-align:center'>👤</div>",
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown(f"""
            <div style="
                background-color:#1c1f26;
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
                border:1px solid #2d3748;
            ">
            <h4>{row['Giocatore']}</h4>
            🌍 {row['Squadra']} <br>
            ⚽ Gol: {row['Gol']} <br>
            🎯 Assist: {row['Assist']}
            </div>
            """, unsafe_allow_html=True)

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