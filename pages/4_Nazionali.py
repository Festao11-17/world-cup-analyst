import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title("🌍 Nazionali")

# CARICAMENTO DATI
df_teams = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

# SELEZIONE NAZIONALE
teams = df_teams["Squadra"].tolist()
selected_team = st.selectbox("Seleziona una Nazionale", teams)

team_data = df_teams[df_teams["Squadra"] == selected_team].iloc[0]
team_players = df_players[df_players["Squadra"] == selected_team]

st.markdown("---")

# HEADER NAZIONALE
st.subheader(f"🏳️ {selected_team}")

# KPI PRINCIPALI
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("⚽ Gol/Partita", team_data["Gol"])
col2.metric("📐 xG", team_data["xG"])
col3.metric("🎯 Tiri", team_data["Tiri"])
col4.metric("🔵 Possesso", f"{team_data['Possesso']}%")
col5.metric("✅ Precisione Passaggi", f"{team_data['PrecisionePassaggi']}%")

st.markdown("---")

# RADAR CHART — confronto vs media globale
st.subheader("📈 Statistiche vs Media Mondiale")

stats = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]
team_values = [team_data[stat] for stat in stats]
avg_values = [df_teams[stat].mean() for stat in stats]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=team_values,
    theta=stats,
    fill='toself',
    name=selected_team,
    line_color='#1f77b4'
))
fig_radar.add_trace(go.Scatterpolar(
    r=avg_values,
    theta=stats,
    fill='toself',
    name='Media Mondiale',
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

# ROSA GIOCATORI
if not team_players.empty:
    st.subheader(f"👥 Rosa — {selected_team}")

    # Riepilogo rosa
    col1, col2, col3 = st.columns(3)
    col1.metric("Giocatori", len(team_players))
    col2.metric("Gol Totali Rosa", int(team_players["Gol"].sum()))
    col3.metric("Assist Totali Rosa", int(team_players["Assist"].sum()))

    st.markdown("#### Statistiche Giocatori")

    # Tabella
    display_cols = ["Giocatore", "Ruolo", "Età", "Presenze", "Gol", "Assist", "xG", "Velocita"]
    st.dataframe(
        team_players[display_cols].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # BAR CHART — Gol per giocatore
    st.subheader("🥇 Gol per Giocatore")
    fig_bar = px.bar(
        team_players.sort_values("Gol", ascending=False),
        x="Giocatore",
        y="Gol",
        color="Ruolo",
        text="Gol",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=True, height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

    # SCATTER — xG vs Gol
    st.subheader("📊 xG vs Gol Reali")
    fig_scatter = px.scatter(
        team_players,
        x="xG",
        y="Gol",
        text="Giocatore",
        color="Ruolo",
        size="Presenze",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_layout(height=380)
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("Nessun giocatore disponibile per questa nazionale.")

st.markdown("---")

# CLASSIFICA GENERALE — posizione della nazionale
st.subheader("🏆 Ranking Nazionali per Gol")
df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
df_ranked.index += 1
df_ranked.index.name = "Pos"

# Evidenzia la nazionale selezionata
def highlight_team(row):
    return ['background-color: #1f4e79; color: white' if row["Squadra"] == selected_team else '' for _ in row]

st.dataframe(
    df_ranked[["Squadra", "Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]].style.apply(highlight_team, axis=1),
    use_container_width=True
)