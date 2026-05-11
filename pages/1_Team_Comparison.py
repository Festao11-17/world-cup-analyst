import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📊 Confronto Nazionali")

# DATI
df = pd.read_csv("data/team_stats.csv")

# LISTA SQUADRE
teams = df["Squadra"].tolist()

# SELECT
team1 = st.selectbox(
    "Seleziona Nazionale 1",
    teams
)

team2 = st.selectbox(
    "Seleziona Nazionale 2",
    teams,
    index=1
)

# DATI SQUADRE
team1_data = df[df["Squadra"] == team1].iloc[0]
team2_data = df[df["Squadra"] == team2].iloc[0]

team1_flag = f"assets/flags/{team1.lower()}.png"
team2_flag = f"assets/flags/{team2.lower()}.png"

st.markdown("---")

# METRICHE
col1, col2 = st.columns(2)

with col1:

    st.image(team1_flag, width=100)

    st.subheader(team1)

    st.metric("Gol", team1_data["Gol"])
    st.metric("xG", team1_data["xG"])
    st.metric("Possesso", f"{team1_data['Possesso']}%")

with col2:

    st.image(team2_flag, width=100)

    st.subheader(team2)

    st.metric("Gol", team2_data["Gol"])
    st.metric("xG", team2_data["xG"])
    st.metric("Possesso", f"{team2_data['Possesso']}%")

st.markdown("---")

# STATS
stats = [
    "Gol",
    "xG",
    "Tiri",
    "Possesso",
    "PrecisionePassaggi"
]

team1_values = [team1_data[stat] for stat in stats]
team2_values = [team2_data[stat] for stat in stats]

# PREDICTION SCORE

team1_score = (
    team1_data["Gol"] * 0.4 +
    team1_data["xG"] * 0.3 +
    team1_data["Possesso"] * 0.2 +
    team1_data["PrecisionePassaggi"] * 0.1
)

team2_score = (
    team2_data["Gol"] * 0.4 +
    team2_data["xG"] * 0.3 +
    team2_data["Possesso"] * 0.2 +
    team2_data["PrecisionePassaggi"] * 0.1
)

total = team1_score + team2_score

team1_probability = round((team1_score / total) * 100)
team2_probability = round((team2_score / total) * 100)

# RADAR
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=team1_values,
    theta=stats,
    fill='toself',
    name=team1
))

fig.add_trace(go.Scatterpolar(
    r=team2_values,
    theta=stats,
    fill='toself',
    name=team2
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

st.markdown("---")

st.subheader("🔮 Match Prediction")

st.markdown(f"""
<div style="
    background-color:#1c1f26;
    border-radius:15px;
    overflow:hidden;
    height:35px;
    display:flex;
    margin-bottom:20px;
">

<div style="
    width:{team1_probability}%;
    background:#3b82f6;
    text-align:center;
    color:white;
    line-height:35px;
    font-weight:bold;
">
{team1_probability}%
</div>

<div style="
    width:{team2_probability}%;
    background:#ef4444;
    text-align:center;
    color:white;
    line-height:35px;
    font-weight:bold;
">
{team2_probability}%
</div>

</div>
""", unsafe_allow_html=True)

col_pred1, col_pred2 = st.columns(2)

with col_pred1:
    st.metric(team1, f"{team1_probability}%")

with col_pred2:
    st.metric(team2, f"{team2_probability}%")

st.subheader("📈 Confronto Statistiche")

st.plotly_chart(fig, use_container_width=True)