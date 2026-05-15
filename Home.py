import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="World Cup Analyst",
    page_icon="assets/logo.png",   # ← stesso file del logo = favicon aggiornata
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FLAG_MAP COMPLETO — 48 SQUADRE FIFA WORLD CUP 2026
# ══════════════════════════════════════════════════════════════════
FLAG_MAP = {
    # Girone A
    "Cechia":           "Girone_A/Cechia",
    "Corea del Sud":    "Girone_A/Corea_del_Sud",
    "Messico":          "Girone_A/Messico",
    "Sudafrica":        "Girone_A/Sudafrica",
    # Girone B
    "Bosnia":           "Girone_B/Bosnia_ed_Erzegovina",
    "Canada":           "Girone_B/Canada",
    "Qatar":            "Girone_B/Qatar",
    "Svizzera":         "Girone_B/Svizzera",
    # Girone C
    "Brasile":          "Girone_C/Brasile",
    "Haiti":            "Girone_C/Haiti",
    "Marocco":          "Girone_C/Marocco",
    "Scozia":           "Girone_C/Scozia",
    # Girone D
    "Australia":        "Girone_D/Australia",
    "Paraguay":         "Girone_D/Paraguay",
    "USA":              "Girone_D/Stati_Uniti",
    "Turchia":          "Girone_D/Turchia",
    # Girone E
    "Costa d'Avorio":   "Girone_E/Costa_d'Avorio",
    "Curacao":          "Girone_E/Curacao",
    "Ecuador":          "Girone_E/Ecuador",
    "Germania":         "Girone_E/Germania",
    # Girone F
    "Giappone":         "Girone_F/Giappone",
    "Olanda":           "Girone_F/Olanda",
    "Svezia":           "Girone_F/Svezia",
    "Tunisia":          "Girone_F/Tunisia",
    # Girone G
    "Belgio":           "Girone_G/Belgio",
    "Egitto":           "Girone_G/Egitto",
    "Iran":             "Girone_G/Iran",
    "Nuova Zelanda":    "Girone_G/Nuova_Zelanda",
    # Girone H
    "Arabia Saudita":   "Girone_H/Arabia_Saudita",
    "Capo Verde":       "Girone_H/Capo_Verde",
    "Spagna":           "Girone_H/Spagna",
    "Uruguay":          "Girone_H/Uruguay",
    # Girone I
    "Francia":          "Girone_I/Francia",
    "Iraq":             "Girone_I/Iraq",
    "Norvegia":         "Girone_I/Norvegia",
    "Senegal":          "Girone_I/Senegal",
    # Girone J
    "Algeria":          "Girone_J/Algeria",
    "Argentina":        "Girone_J/Argentina",
    "Austria":          "Girone_J/Austria",
    "Giordania":        "Girone_J/Giordania",
    # Girone K
    "Colombia":         "Girone_K/Colombia",
    "Portogallo":       "Girone_K/Portogallo",
    "Rep. del Congo":   "Girone_K/Repubblica_del_Congo",
    "Uzbekistan":       "Girone_K/Uzbekistan",
    # Girone L
    "Croazia":          "Girone_L/Croazia",
    "Ghana":            "Girone_L/Ghana",
    "Inghilterra":      "Girone_L/Inghilterra",
    "Panama":           "Girone_L/Panama",
}

def flag_path(s): return f"assets/flags/{FLAG_MAP.get(s, s)}.png"
def flag_img(squadra, width=32):
    p = flag_path(squadra)
    if os.path.exists(p):
        return st.image(p, width=width)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=100)
    st.markdown("### WORLD CUP\nANALYST")
    st.markdown("---")
    st.markdown(
        "<span class='wca-badge'>FIFA WORLD CUP 2026</span>",
        unsafe_allow_html=True
    )

# ── DATI ─────────────────────────────────────────────────────────────────────
df_teams   = pd.read_csv("data/team_stats.csv")
df_players = pd.read_csv("data/world_cup_players.csv")

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 20px;">
  <div style="color:#6b7a99;font-size:11px;letter-spacing:3px;text-transform:uppercase;font-weight:600;margin-bottom:8px;">
    FIFA WORLD CUP 2026 · ANALYTICS PLATFORM
  </div>
  <h1 style="font-size:4rem;margin:0;line-height:1">WORLD CUP<br>ANALYST</h1>
  <p style="color:#6b7a99;margin-top:12px;font-size:15px;max-width:500px">
    Statistiche avanzate, radar, profili e previsioni per tutte le 48 nazionali del Mondiale 2026.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── TOP STATS ────────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>📊 Top Stats</span>", unsafe_allow_html=True)

best_attack = df_teams.loc[df_teams["Gol"].idxmax()]
best_xg     = df_teams.loc[df_teams["xG"].idxmax()]
best_poss   = df_teams.loc[df_teams["Possesso"].idxmax()]
top_scorer  = df_players.loc[df_players["Gol"].idxmax()]
top_assist  = df_players.loc[df_players["Assist"].idxmax()]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Miglior Attacco",  best_attack["Squadra"],  f"{best_attack['Gol']} gol/match")
c2.metric("📐 Miglior xG",       best_xg["Squadra"],      f"xG {best_xg['xG']}")
c3.metric("🔵 Miglior Possesso", best_poss["Squadra"],    f"{best_poss['Possesso']}%")
c4.metric("🥇 Capocannoniere",   top_scorer["Giocatore"], f"{int(top_scorer['Gol'])} gol")
c5.metric("🎯 Top Assistman",    top_assist["Giocatore"], f"{int(top_assist['Assist'])} assist")

st.markdown("---")

# ── FEATURED MATCH ───────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🔥 Featured Match</span>", unsafe_allow_html=True)

top2 = df_teams.nlargest(2, "Gol")
t1, t2 = top2.iloc[0], top2.iloc[1]
stats  = ["Gol", "xG", "Tiri", "Possesso", "PrecisionePassaggi"]

col_l, col_c, col_r = st.columns([3, 1, 3])
with col_l:
    fp = flag_path(t1["Squadra"])
    if os.path.exists(fp): st.image(fp, width=56)
    st.markdown(f"### {t1['Squadra']}")
    ca, cb, cc = st.columns(3)
    ca.metric("Gol", t1["Gol"]); cb.metric("xG", t1["xG"]); cc.metric("Poss.", f"{t1['Possesso']}%")

with col_c:
    st.markdown(
        "<div style='text-align:center;padding-top:40px'>"
        "<div style='font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:#6b7a99;letter-spacing:3px'>VS</div>"
        "<div style='width:1px;height:60px;background:#1f2d45;margin:8px auto'></div>"
        "</div>",
        unsafe_allow_html=True
    )

with col_r:
    fp2 = flag_path(t2["Squadra"])
    if os.path.exists(fp2): st.image(fp2, width=56)
    st.markdown(f"### {t2['Squadra']}")
    ca, cb, cc = st.columns(3)
    ca.metric("Gol", t2["Gol"]); cb.metric("xG", t2["xG"]); cc.metric("Poss.", f"{t2['Possesso']}%")

fig = go.Figure()
for team, color in [(t1, "#00d4ff"), (t2, "#ff3b5c")]:
    fig.add_trace(go.Scatterpolar(
        r=[team[s] for s in stats], theta=stats,
        fill='toself', name=team["Squadra"],
        line=dict(color=color, width=2),
        fillcolor=color.replace("ff", "22") if "#" in color else color,
        opacity=0.85
    ))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(26,32,53,0.6)",
        radialaxis=dict(visible=True, gridcolor="#1f2d45", color="#6b7a99", linecolor="#1f2d45"),
        angularaxis=dict(gridcolor="#1f2d45", color="#6b7a99", linecolor="#1f2d45")
    ),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e8edf5")),
    height=380, margin=dict(t=30, b=30)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ── LEADERBOARD ──────────────────────────────────────────────────────────────
st.markdown("<span class='wca-section-label'>🏆 Leaderboard</span>", unsafe_allow_html=True)

col_lb, col_pl = st.columns(2)
medals = {0: "🥇", 1: "🥈", 2: "🥉"}

with col_lb:
    st.markdown("#### Ranking Nazionali")
    df_ranked = df_teams.sort_values("Gol", ascending=False).reset_index(drop=True)
    for i, row in df_ranked.iterrows():
        medal = medals.get(i, f"{i+1}.")
        fp = flag_path(row["Squadra"])
        c1, c2 = st.columns([1, 6])
        with c1:
            if os.path.exists(fp): st.image(fp, width=28)
            else: st.write(medal)
        with c2:
            st.markdown(
                f"<div class='wca-card' style='padding:10px 16px;margin-bottom:6px'>"
                f"<b>{medal} {row['Squadra']}</b>"
                f"<div class='wca-stat-row'>"
                f"<div class='wca-stat'>⚽ <span>{row['Gol']}</span></div>"
                f"<div class='wca-stat'>xG <span>{row['xG']}</span></div>"
                f"<div class='wca-stat'>🔵 <span>{row['Possesso']}%</span></div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

with col_pl:
    st.markdown("#### Top Marcatori")
    top8 = df_players.sort_values("Gol", ascending=False).head(8).reset_index(drop=True)
    for i, row in top8.iterrows():
        medal = medals.get(i, f"{i+1}.")
        fp = flag_path(row["Squadra"])
        c1, c2 = st.columns([1, 6])
        with c1:
            if os.path.exists(fp): st.image(fp, width=28)
        with c2:
            st.markdown(
                f"<div class='wca-card' style='padding:10px 16px;margin-bottom:6px'>"
                f"<b>{medal} {row['Giocatore']}</b> "
                f"<span style='color:#6b7a99;font-size:12px'>{row['Squadra']}</span>"
                f"<div class='wca-stat-row'>"
                f"<div class='wca-stat'>⚽ <span>{int(row['Gol'])}</span></div>"
                f"<div class='wca-stat'>🎯 <span>{int(row['Assist'])}</span></div>"
                f"<div class='wca-stat'>xG <span>{row['xG']}</span></div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

st.markdown("---")

# ── NAV CARDS — cliccabili desktop e mobile via st.page_link ─────────────────
st.markdown("<span class='wca-section-label'>📂 Sezioni</span>", unsafe_allow_html=True)

# CSS extra: rende i page_link simili alle wca-card
st.markdown("""
<style>
/* Wrapper del page_link → aspetto card */
[data-testid="stPageLink"] > a {
  display: block !important;
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-lg) !important;
  padding: 20px 14px !important;
  text-align: center !important;
  text-decoration: none !important;
  color: var(--text) !important;
  transition: border-color 0.2s, transform 0.15s !important;
  min-height: 100px !important;
}
[data-testid="stPageLink"] > a:hover {
  border-color: var(--cyan) !important;
  transform: translateY(-2px) !important;
}
[data-testid="stPageLink"] p {
  color: var(--text) !important;
  font-size: 13px !important;
  margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

sections = [
    ("🌍", "Nazionali",         "Cerca giocatori per squadra",      "pages/4_Nazionali.py"),
    ("🏳️", "Team Profile",      "Scheda di ogni nazionale",          "pages/7_Team_Profile.py"),
    ("🌟", "Player Profile",    "Profilo dettagliato giocatore",     "pages/6_Player_Profile.py"),
    ("📊", "Team Comparison",   "Confronto radar tra nazionali",     "pages/1_Team_Comparison.py"),
    ("👤", "Player Comparison", "Confronto statistiche giocatori",   "pages/2_Player_Comparison.py"),
    ("🔮", "Predictions",       "Predizioni basate sui dati",        "pages/3_Match_Predictions.py"),
    ("🏅", "Power Rankings",    "Classifica forza nazionali",        "pages/8_Power_Rankings.py"),
    ("🌐", "WC Simulator",      "Simula l'intero torneo",            "pages/9_WC_Simulator.py"),
    ("🔍", "Scouting",          "Scopri talenti per ruolo",          "pages/5_Player_Scouting.py"),
]

# Griglia 3 colonne: funziona meglio su mobile rispetto a 5 o 9 colonne piatte
rows = [sections[i:i+3] for i in range(0, len(sections), 3)]
for row_sections in rows:
    cols = st.columns(3)
    for col, (icon, title, desc, page_path) in zip(cols, row_sections):
        with col:
            st.page_link(
                page_path,
                label=f"{icon} **{title}**\n\n*{desc}*",
                use_container_width=True,
            )