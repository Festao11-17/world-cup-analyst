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

st.markdown("<h1>🔮 MATCH PREDICTION</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6b7a99;margin-bottom:24px'>Predizioni basate su Power Rating, xG e statistiche avanzate.</p>", unsafe_allow_html=True)

df = pd.read_csv("data/team_stats.csv")
teams = df["Squadra"].tolist()

col1, col2 = st.columns(2)
with col1: team1 = st.selectbox("Squadra Casa", teams, index=0)
with col2: team2 = st.selectbox("Squadra Ospite", teams, index=1)

t1 = df[df["Squadra"] == team1].iloc[0]
t2 = df[df["Squadra"] == team2].iloc[0]

st.markdown("---")

# ── HEADER MATCH ────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([3, 1, 3])

with col_l:
    fp = flag_path(team1)
    if os.path.exists(fp): st.image(fp, width=70)
    st.markdown(f"### {team1}")
    st.markdown(
        f"<span class='wca-badge'>⭐ {t1['OverallRating']} Overall</span>",
        unsafe_allow_html=True
    )

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:36px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "</div>", unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(team2)
    if os.path.exists(fp2): st.image(fp2, width=70)
    st.markdown(f"### {team2}")
    st.markdown(
        f"<span class='wca-badge'>⭐ {t2['OverallRating']} Overall</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── CALCOLO PREDICTION con Power Rating ────────────────────────────────────
# Overall 50% + Attack 25% + Midfield 15% + Defense 10%
s1 = (t1["OverallRating"] * 0.50 + t1["AttackRating"] * 0.25 +
      t1["MidfieldRating"] * 0.15 + t1["DefenseRating"] * 0.10)
s2 = (t2["OverallRating"] * 0.50 + t2["AttackRating"] * 0.25 +
      t2["MidfieldRating"] * 0.15 + t2["DefenseRating"] * 0.10)

total = s1 + s2
p1 = round((s1 / total) * 100, 1)
p2 = round((s2 / total) * 100, 1)
draw = round(max(0, 35 - abs(p1 - p2) * 0.8), 1)

# Ribilancia togliendo il pareggio proporzionalmente
factor = (100 - draw) / 100
p1_adj = round(p1 * factor, 1)
p2_adj = round(p2 * factor, 1)

# Score prediction basato su xG e attack rating
import math
xg1 = round(t1["xG"] * (t1["AttackRating"] / 75), 1)
xg2 = round(t2["xG"] * (t2["AttackRating"] / 75), 1)
goals1 = int(round(xg1 * 0.85))
goals2 = int(round(xg2 * 0.85))

# ── WIN PROBABILITY ─────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Win Probability</span>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric(f"🏆 {team1}", f"{p1_adj}%")
c2.metric("🤝 Pareggio", f"{draw}%")
c3.metric(f"🏆 {team2}", f"{p2_adj}%")

# Barra probabilità visiva
bar_html = f"""
<div style='margin:16px 0 8px;display:flex;border-radius:8px;overflow:hidden;height:28px'>
  <div style='width:{p1_adj}%;background:#00d4ff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700'>{p1_adj}%</div>
  <div style='width:{draw}%;background:#1f2d45;display:flex;align-items:center;justify-content:center;font-size:12px;color:#6b7a99'>{draw}%</div>
  <div style='width:{p2_adj}%;background:#ff3b5c;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700'>{p2_adj}%</div>
</div>
<div style='display:flex;justify-content:space-between;font-size:11px;color:#6b7a99;margin-bottom:8px'>
  <span>{team1}</span><span>Pareggio</span><span>{team2}</span>
</div>
"""
st.markdown(bar_html, unsafe_allow_html=True)

st.markdown("---")

# ── SCORE PREDICTION ────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>⚽ Risultato Previsto</span>", unsafe_allow_html=True)

col_s1, col_score, col_s2 = st.columns([2, 1, 2])
with col_s1:
    st.markdown(
        f"<div class='wca-card' style='text-align:center'>"
        f"<div style='font-size:11px;color:#6b7a99;text-transform:uppercase;letter-spacing:1px'>xG Previsto</div>"
        f"<div style='font-size:3rem;font-family:Bebas Neue,sans-serif;color:#00d4ff'>{xg1}</div>"
        f"<div style='font-size:12px;color:#6b7a99'>{team1}</div>"
        f"</div>", unsafe_allow_html=True
    )
with col_score:
    st.markdown(
        f"<div style='text-align:center;padding-top:20px'>"
        f"<div style='font-family:Bebas Neue,sans-serif;font-size:3.5rem;letter-spacing:4px'>{goals1} - {goals2}</div>"
        f"<div style='color:#6b7a99;font-size:11px;text-transform:uppercase;letter-spacing:2px'>Pronostico</div>"
        f"</div>", unsafe_allow_html=True
    )
with col_s2:
    st.markdown(
        f"<div class='wca-card' style='text-align:center'>"
        f"<div style='font-size:11px;color:#6b7a99;text-transform:uppercase;letter-spacing:1px'>xG Previsto</div>"
        f"<div style='font-size:3rem;font-family:Bebas Neue,sans-serif;color:#ff3b5c'>{xg2}</div>"
        f"<div style='font-size:12px;color:#6b7a99'>{team2}</div>"
        f"</div>", unsafe_allow_html=True
    )

st.markdown("---")

# ── ANALISI RATING ──────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📈 Analisi per Reparto</span>", unsafe_allow_html=True)

for label, r1, r2, color1, color2 in [
    ("⚔️ Attacco",     t1["AttackRating"],   t2["AttackRating"],   "#ff3b5c", "#ff3b5c"),
    ("🔄 Centrocampo", t1["MidfieldRating"],  t2["MidfieldRating"], "#00d4ff", "#00d4ff"),
    ("🛡️ Difesa",      t1["DefenseRating"],   t2["DefenseRating"],  "#00e5a0", "#00e5a0"),
    ("⭐ Overall",     t1["OverallRating"],   t2["OverallRating"],  "#f39c12", "#f39c12"),
]:
    winner_color = "#00d4ff" if r1 > r2 else ("#ff3b5c" if r2 > r1 else "#6b7a99")
    max_r = max(r1, r2, 95)

    st.markdown(
        f"<div style='margin-bottom:14px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='font-weight:700;color:{'#00d4ff' if r1>=r2 else '#6b7a99'}'>{r1}</span>"
        f"<span style='font-size:12px;color:#6b7a99'>{label}</span>"
        f"<span style='font-weight:700;color:{'#ff3b5c' if r2>r1 else '#6b7a99'}'>{r2}</span>"
        f"</div>"
        f"<div style='display:flex;gap:4px'>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px;display:flex;justify-content:flex-end'>"
        f"<div style='width:{int(r1/max_r*100)}%;background:#00d4ff;border-radius:4px;height:8px'></div></div>"
        f"<div style='flex:1;background:#1f2d45;border-radius:4px;height:8px'>"
        f"<div style='width:{int(r2/max_r*100)}%;background:#ff3b5c;border-radius:4px;height:8px'></div></div>"
        f"</div></div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ── RADAR CONFRONTO ─────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📡 Radar Confronto</span>", unsafe_allow_html=True)

stats  = ["Gol","xG","Tiri","Possesso","PrecisionePassaggi"]
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
    height=400, showlegend=True
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# ── MATCH INSIGHTS ──────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>💡 Match Insights</span>", unsafe_allow_html=True)

insights = []

# Attacco
att_diff = t1["AttackRating"] - t2["AttackRating"]
if att_diff >= 8:
    insights.append(("⚔️", f"{team1} ha un attacco nettamente superiore ({t1['AttackRating']} vs {t2['AttackRating']}).", "cyan"))
elif att_diff <= -8:
    insights.append(("⚔️", f"{team2} ha un attacco nettamente superiore ({t2['AttackRating']} vs {t1['AttackRating']}).", "red"))
else:
    insights.append(("⚔️", f"Attacchi molto equilibrati ({t1['AttackRating']} vs {t2['AttackRating']}).", "muted"))

# Centrocampo
mid_diff = t1["MidfieldRating"] - t2["MidfieldRating"]
if mid_diff >= 8:
    insights.append(("🔄", f"{team1} domina il centrocampo ({t1['MidfieldRating']} vs {t2['MidfieldRating']}).", "cyan"))
elif mid_diff <= -8:
    insights.append(("🔄", f"{team2} domina il centrocampo ({t2['MidfieldRating']} vs {t1['MidfieldRating']}).", "red"))
else:
    insights.append(("🔄", f"Centrocampo equilibrato ({t1['MidfieldRating']} vs {t2['MidfieldRating']}).", "muted"))

# Difesa
def_diff = t1["DefenseRating"] - t2["DefenseRating"]
if def_diff >= 8:
    insights.append(("🛡️", f"{team1} ha una difesa più solida ({t1['DefenseRating']} vs {t2['DefenseRating']}).", "cyan"))
elif def_diff <= -8:
    insights.append(("🛡️", f"{team2} ha una difesa più solida ({t2['DefenseRating']} vs {t1['DefenseRating']}).", "red"))
else:
    insights.append(("🛡️", f"Difese simili per solidità ({t1['DefenseRating']} vs {t2['DefenseRating']}).", "muted"))

# xG
xg_diff = t1["xG"] - t2["xG"]
if xg_diff >= 0.3:
    insights.append(("📐", f"{team1} crea occasioni di maggior qualità (xG {t1['xG']} vs {t2['xG']}).", "cyan"))
elif xg_diff <= -0.3:
    insights.append(("📐", f"{team2} crea occasioni di maggior qualità (xG {t2['xG']} vs {t1['xG']}).", "red"))
else:
    insights.append(("📐", f"xG molto simile — partita che si decide nei dettagli.", "muted"))

# Possesso
pos_diff = t1["Possesso"] - t2["Possesso"]
if pos_diff >= 5:
    insights.append(("🔵", f"{team1} tende a controllare il pallone ({t1['Possesso']}% vs {t2['Possesso']}%).", "cyan"))
elif pos_diff <= -5:
    insights.append(("🔵", f"{team2} tende a controllare il pallone ({t2['Possesso']}% vs {t1['Possesso']}%).", "red"))

# Overall gap
overall_diff = abs(t1["OverallRating"] - t2["OverallRating"])
if overall_diff < 3:
    insights.append(("⚡", "Gap minimo tra le due squadre — pronostico apertissimo.", "muted"))
elif overall_diff >= 12:
    stronger = team1 if t1["OverallRating"] > t2["OverallRating"] else team2
    insights.append(("⚡", f"{stronger} è la favorita su tutti i fronti.", "cyan" if stronger == team1 else "red"))

color_map = {"cyan": "#00d4ff", "red": "#ff3b5c", "muted": "#6b7a99"}

for emoji, text, color_key in insights:
    color = color_map[color_key]
    st.markdown(
        f"<div class='wca-card' style='padding:12px 18px;margin-bottom:8px;border-left:3px solid {color}'>"
        f"<span style='margin-right:10px'>{emoji}</span>"
        f"<span style='color:{color};font-size:14px'>{text}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

st.markdown("---")
# ── VERDETTO ────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🏆 Verdetto</span>", unsafe_allow_html=True)

diff = abs(t1["OverallRating"] - t2["OverallRating"])
if p1_adj > p2_adj:
    fav, und = team1, team2
    fav_p, und_p = p1_adj, p2_adj
else:
    fav, und = team2, team1
    fav_p, und_p = p2_adj, p1_adj

if diff >= 10:
    verdict = f"<span class='wca-badge'>🟢 FAVORITA NETTA</span> &nbsp; <b>{fav}</b> domina su carta con un gap di <b>{diff:.1f} punti</b> di rating."
elif diff >= 5:
    verdict = f"<span class='wca-badge'>🟡 LEGGERO VANTAGGIO</span> &nbsp; <b>{fav}</b> parte leggermente favorita ({fav_p}% vs {und_p}%), ma la partita è aperta."
else:
    verdict = f"<span class='wca-badge wca-badge-red'>🔴 EQUILIBRIO TOTALE</span> &nbsp; Gap di soli <b>{diff:.1f} punti</b>. Partita da dentro o fuori, ogni dettaglio conta."

st.markdown(f"<div class='wca-card'>{verdict}</div>", unsafe_allow_html=True)