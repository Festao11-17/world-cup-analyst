import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title("🌟 Profilo Giocatore")

# CARICAMENTO DATI
df = pd.read_csv("data/world_cup_players.csv")
df_teams = pd.read_csv("data/team_stats.csv")

players = df["Giocatore"].tolist()

# SELECTBOX
selected_player = st.selectbox("Seleziona un Giocatore", players)

player = df[df["Giocatore"] == selected_player].iloc[0]

st.markdown("---")

# ── HEADER PROFILO ─────────────────────────────────────────────────────────
col_img, col_info = st.columns([1, 3])

with col_img:
    player_image = f"assets/players/{selected_player.lower()}.png"
    if os.path.exists(player_image):
        st.image(player_image, width=180)
    else:
        st.markdown(
            "<div style='font-size:100px;text-align:center'>👤</div>",
            unsafe_allow_html=True
        )

with col_info:
    st.markdown(f"## {selected_player}")
    st.markdown(f"**🌍 Nazionale:** {player['Squadra']}")
    st.markdown(f"**🎽 Ruolo:** {player['Ruolo']}")
    st.markdown(f"**🎂 Età:** {player['Età']} anni")
    st.markdown(f"**📋 Presenze:** {player['Presenze']}")

st.markdown("---")

# ── KPI ────────────────────────────────────────────────────────────────────
st.subheader("📊 Statistiche Principali")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Gol",      int(player["Gol"]))
c2.metric("🎯 Assist",   int(player["Assist"]))
c3.metric("📐 xG",       player["xG"])
c4.metric("🎯 Tiri",     int(player["Tiri"]))
c5.metric("⚡ Velocità", int(player["Velocita"]))

st.markdown("---")

# ── RADAR ──────────────────────────────────────────────────────────────────
st.subheader("📈 Radar vs Media Ruolo")

stats = ["Gol", "Assist", "xG", "Tiri", "Velocita"]

# Media dei giocatori dello stesso ruolo
same_role = df[df["Ruolo"] == player["Ruolo"]]
avg_values = [same_role[s].mean() for s in stats]
player_values = [player[s] for s in stats]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=player_values,
    theta=stats,
    fill='toself',
    name=selected_player,
    line_color='#1f77b4'
))
fig_radar.add_trace(go.Scatterpolar(
    r=avg_values,
    theta=stats,
    fill='toself',
    name=f"Media {player['Ruolo']}",
    line_color='#aaa',
    opacity=0.5
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=400
)
st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# ── CONFRONTO AUTOMATICO ───────────────────────────────────────────────────
st.subheader("⚔️ Confronto Automatico — Stesso Ruolo")

# Top 5 giocatori dello stesso ruolo per gol (escluso il giocatore selezionato)
rivals = df[
    (df["Ruolo"] == player["Ruolo"]) &
    (df["Giocatore"] != selected_player)
].sort_values("Gol", ascending=False).head(5)

if rivals.empty:
    st.info("Nessun altro giocatore dello stesso ruolo disponibile.")
else:
    # Bar chart gol a confronto
    compare_df = pd.concat([
        pd.DataFrame([player]),
        rivals
    ]).reset_index(drop=True)

    colors = ["#1f77b4" if g == selected_player else "#adb5bd"
              for g in compare_df["Giocatore"]]

    fig_bar = go.Figure(go.Bar(
        x=compare_df["Giocatore"],
        y=compare_df["Gol"],
        marker_color=colors,
        text=compare_df["Gol"],
        textposition="outside"
    ))
    fig_bar.update_layout(
        title="Gol — confronto con stesso ruolo",
        height=350,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Scatter xG vs Gol
    fig_scatter = px.scatter(
        compare_df,
        x="xG",
        y="Gol",
        text="Giocatore",
        size="Presenze",
        color=compare_df["Giocatore"].apply(
            lambda x: selected_player if x == selected_player else "Altri"
        ),
        color_discrete_map={selected_player: "#1f77b4", "Altri": "#adb5bd"},
        title="xG vs Gol reali"
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_layout(height=380, showlegend=True)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ── INFO NAZIONALE ─────────────────────────────────────────────────────────
st.subheader(f"🏳️ La sua Nazionale — {player['Squadra']}")

team_row = df_teams[df_teams["Squadra"] == player["Squadra"]]

if not team_row.empty:
    t = team_row.iloc[0]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("⚽ Gol/Partita",   t["Gol"])
    c2.metric("📐 xG",            t["xG"])
    c3.metric("🎯 Tiri",          t["Tiri"])
    c4.metric("🔵 Possesso",      f"{t['Possesso']}%")
    c5.metric("✅ Precisione",    f"{t['PrecisionePassaggi']}%")

    # Compagni di squadra
    teammates = df[
        (df["Squadra"] == player["Squadra"]) &
        (df["Giocatore"] != selected_player)
    ].sort_values("Gol", ascending=False)

    if not teammates.empty:
        st.markdown("#### 👥 Compagni di Squadra")
        st.dataframe(
            teammates[["Giocatore", "Ruolo", "Età", "Gol", "Assist", "xG"]].reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )